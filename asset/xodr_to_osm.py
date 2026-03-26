#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

from pyproj import CRS, Transformer


NS = {"x": "http://www.opendrive.org"}


@dataclass
class WidthSegment:
    s_offset: float
    a: float
    b: float
    c: float
    d: float

    def value(self, ds: float) -> float:
        return self.a + self.b * ds + self.c * ds * ds + self.d * ds * ds * ds


@dataclass
class LaneData:
    lane_id: int
    lane_type: str
    widths: list[WidthSegment]


@dataclass
class GeometryPoint:
    s: float
    x: float
    y: float
    hdg: float


@dataclass
class LaneletGeometry:
    subtype: str
    left_coords: list[tuple[float, float]]
    right_coords: list[tuple[float, float]]


def read_proj4(root: ET.Element) -> str:
    header = root.find("x:header", NS)
    if header is None:
        raise ValueError("OpenDRIVE header not found")
    geo_ref = header.find("x:geoReference", NS)
    if geo_ref is None or not (geo_ref.text and geo_ref.text.strip()):
        raise ValueError("OpenDRIVE geoReference not found")
    return geo_ref.text.strip()


def sample_geometry(geom: ET.Element, step: float) -> list[GeometryPoint]:
    s0 = float(geom.attrib["s"])
    x0 = float(geom.attrib["x"])
    y0 = float(geom.attrib["y"])
    hdg0 = float(geom.attrib["hdg"])
    length = float(geom.attrib["length"])

    line = geom.find("x:line", NS)
    arc = geom.find("x:arc", NS)
    samples = max(1, math.ceil(length / step))

    points: list[GeometryPoint] = []
    for i in range(samples + 1):
        u = min(i * step, length)
        if line is not None:
            x = x0 + u * math.cos(hdg0)
            y = y0 + u * math.sin(hdg0)
            hdg = hdg0
        elif arc is not None:
            k = float(arc.attrib["curvature"])
            if abs(k) < 1e-12:
                x = x0 + u * math.cos(hdg0)
                y = y0 + u * math.sin(hdg0)
                hdg = hdg0
            else:
                hdg = hdg0 + k * u
                x = x0 + (math.sin(hdg) - math.sin(hdg0)) / k
                y = y0 + (math.cos(hdg0) - math.cos(hdg)) / k
        else:
            raise ValueError("Unsupported geometry: only <line/> and <arc/> are handled")
        points.append(GeometryPoint(s=s0 + u, x=x, y=y, hdg=hdg))
    return points


def sample_reference_line(road: ET.Element, step: float) -> list[GeometryPoint]:
    points: list[GeometryPoint] = []
    for geom in road.findall("x:planView/x:geometry", NS):
        geom_points = sample_geometry(geom, step)
        if points:
            geom_points = geom_points[1:]
        points.extend(geom_points)
    return points


def read_lane_offset_sections(road: ET.Element) -> list[WidthSegment]:
    sections = []
    for lane_offset in road.findall("x:lanes/x:laneOffset", NS):
        sections.append(
            WidthSegment(
                s_offset=float(lane_offset.attrib["s"]),
                a=float(lane_offset.attrib["a"]),
                b=float(lane_offset.attrib["b"]),
                c=float(lane_offset.attrib["c"]),
                d=float(lane_offset.attrib["d"]),
            )
        )
    if not sections:
        sections.append(WidthSegment(0.0, 0.0, 0.0, 0.0, 0.0))
    sections.sort(key=lambda item: item.s_offset)
    return sections


def eval_piecewise_poly(sections: list[WidthSegment], s: float) -> float:
    current = sections[0]
    for section in sections:
        if section.s_offset <= s:
            current = section
        else:
            break
    ds = s - current.s_offset
    return current.value(ds)


def parse_lane(lane: ET.Element) -> LaneData:
    widths = [
        WidthSegment(
            s_offset=float(width.attrib["sOffset"]),
            a=float(width.attrib["a"]),
            b=float(width.attrib["b"]),
            c=float(width.attrib["c"]),
            d=float(width.attrib["d"]),
        )
        for width in lane.findall("x:width", NS)
    ]
    widths.sort(key=lambda item: item.s_offset)
    return LaneData(
        lane_id=int(lane.attrib["id"]),
        lane_type=lane.attrib["type"],
        widths=widths,
    )


def lane_width_at(lane: LaneData, lane_section_start_s: float, s: float) -> float:
    if not lane.widths:
        return 0.0
    local_s = s - lane_section_start_s
    return max(0.0, eval_piecewise_poly(lane.widths, local_s))


def collect_lane_section(road: ET.Element) -> tuple[float, dict[int, LaneData]]:
    lane_section = road.find("x:lanes/x:laneSection", NS)
    if lane_section is None:
        return 0.0, {}

    start_s = float(lane_section.attrib["s"])
    lanes: dict[int, LaneData] = {}
    for lane in lane_section.findall("x:left/x:lane", NS):
        data = parse_lane(lane)
        lanes[data.lane_id] = data
    for lane in lane_section.findall("x:right/x:lane", NS):
        data = parse_lane(lane)
        lanes[data.lane_id] = data
    return start_s, lanes


def offset_point(point: GeometryPoint, lateral_offset: float) -> tuple[float, float]:
    x = point.x - lateral_offset * math.sin(point.hdg)
    y = point.y + lateral_offset * math.cos(point.hdg)
    return x, y


def boundary_offsets_for_lane(
    lane_id: int,
    lanes: dict[int, LaneData],
    lane_offset: float,
    lane_section_start_s: float,
    s: float,
) -> tuple[float, float]:
    width = lane_width_at(lanes[lane_id], lane_section_start_s, s)
    if lane_id > 0:
        inner = lane_offset
        for inner_id in sorted(i for i in lanes if 0 < i < lane_id):
            inner += lane_width_at(lanes[inner_id], lane_section_start_s, s)
        outer = inner + width
        return inner, outer

    inner = lane_offset
    for inner_id in sorted((i for i in lanes if lane_id < i < 0), reverse=True):
        inner -= lane_width_at(lanes[inner_id], lane_section_start_s, s)
    outer = inner - width
    return inner, outer


def dedupe_coords(coords: list[tuple[float, float]]) -> list[tuple[float, float]]:
    deduped: list[tuple[float, float]] = []
    last_key: tuple[float, float] | None = None
    for x, y in coords:
        key = (round(x, 6), round(y, 6))
        if key == last_key:
            continue
        deduped.append((x, y))
        last_key = key
    return deduped


def lanelet_subtype(lane_type: str) -> str:
    if lane_type == "sidewalk":
        return "walkway"
    if lane_type == "parking":
        return "parking"
    return "road"


def collect_lanelets(root: ET.Element, step: float) -> list[LaneletGeometry]:
    lanelets: list[LaneletGeometry] = []

    for road in root.findall("x:road", NS):
        lane_section_start_s, lanes = collect_lane_section(road)
        if not lanes:
            continue

        reference_points = sample_reference_line(road, step)
        if not reference_points:
            continue

        lane_offsets = read_lane_offset_sections(road)

        for lane_id in sorted(lanes):
            lane = lanes[lane_id]
            if lane_id == 0 or not lane.widths:
                continue

            left_coords: list[tuple[float, float]] = []
            right_coords: list[tuple[float, float]] = []
            for point in reference_points:
                lateral_shift = eval_piecewise_poly(lane_offsets, point.s)
                inner_offset, outer_offset = boundary_offsets_for_lane(
                    lane_id=lane_id,
                    lanes=lanes,
                    lane_offset=lateral_shift,
                    lane_section_start_s=lane_section_start_s,
                    s=point.s,
                )
                left_coords.append(offset_point(point, inner_offset))
                right_coords.append(offset_point(point, outer_offset))

            if lane_id > 0:
                left_coords.reverse()
                right_coords.reverse()

            left_coords = dedupe_coords(left_coords)
            right_coords = dedupe_coords(right_coords)
            if len(left_coords) < 2 or len(right_coords) < 2:
                continue

            lanelets.append(
                LaneletGeometry(
                    subtype=lanelet_subtype(lane.lane_type),
                    left_coords=left_coords,
                    right_coords=right_coords,
                )
            )

    return lanelets


def build_osm(input_path: Path, output_path: Path, step: float) -> tuple[int, int, int]:
    tree = ET.parse(input_path)
    root = tree.getroot()

    proj4 = read_proj4(root)
    transformer = Transformer.from_crs(CRS.from_proj4(proj4), CRS.from_epsg(4326), always_xy=True)
    lanelets = collect_lanelets(root, step)
    if not lanelets:
        raise ValueError("No lanelets were generated from the input .xodr file")

    osm_root = ET.Element("osm", version="0.6", generator="lanelet2")

    next_id = 1000
    coord_to_node_id: dict[tuple[float, float], int] = {}
    node_records: list[tuple[int, float, float, float, float]] = []

    def get_node_id(x: float, y: float) -> int:
        nonlocal next_id
        key = (round(x, 6), round(y, 6))
        existing = coord_to_node_id.get(key)
        if existing is not None:
            return existing

        node_id = next_id
        next_id += 1
        lon, lat = transformer.transform(x, y)
        coord_to_node_id[key] = node_id
        node_records.append((node_id, x, y, lat, lon))
        return node_id

    lanelet_node_refs: list[tuple[str, list[int], list[int]]] = []
    for lanelet in lanelets:
        left_refs = [get_node_id(x, y) for x, y in lanelet.left_coords]
        right_refs = [get_node_id(x, y) for x, y in lanelet.right_coords]
        lanelet_node_refs.append((lanelet.subtype, left_refs, right_refs))

    way_records: list[tuple[int, list[int]]] = []
    relation_records: list[tuple[int, int, int, str]] = []
    for subtype, left_refs, right_refs in lanelet_node_refs:
        right_way_id = next_id
        next_id += 1
        left_way_id = next_id
        next_id += 1
        relation_id = next_id
        next_id += 1

        way_records.append((right_way_id, right_refs))
        way_records.append((left_way_id, left_refs))
        relation_records.append((relation_id, left_way_id, right_way_id, subtype))

    for node_id, x, y, lat, lon in node_records:
        node = ET.SubElement(
            osm_root,
            "node",
            id=str(node_id),
            visible="true",
            version="1",
            lat=f"{lat:.11f}",
            lon=f"{lon:.11f}",
        )
        ET.SubElement(node, "tag", k="ele", v="0.000000")
        ET.SubElement(node, "tag", k="local_x", v=f"{x:.6f}")
        ET.SubElement(node, "tag", k="local_y", v=f"{y:.6f}")

    for way_id, refs in way_records:
        way = ET.SubElement(osm_root, "way", id=str(way_id), visible="true", version="1")
        for ref in refs:
            ET.SubElement(way, "nd", ref=str(ref))

    for relation_id, left_way_id, right_way_id, subtype in relation_records:
        relation = ET.SubElement(osm_root, "relation", id=str(relation_id), visible="true", version="1")
        ET.SubElement(relation, "member", type="way", ref=str(left_way_id), role="left")
        ET.SubElement(relation, "member", type="way", ref=str(right_way_id), role="right")
        ET.SubElement(relation, "tag", k="subtype", v=subtype)
        ET.SubElement(relation, "tag", k="type", v="lanelet")

    ET.indent(osm_root, space="  ")
    xml_text = ET.tostring(osm_root, encoding="unicode")
    output_path.write_text(f'<?xml version="1.0"?>\n{xml_text}\n', encoding="utf-8")
    return len(node_records), len(way_records), len(relation_records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a subset of OpenDRIVE .xodr to Lanelet2-style OSM XML")
    parser.add_argument("input", type=Path, help="Path to the .xodr file")
    parser.add_argument("output", type=Path, nargs="?", help="Path to the output .osm file")
    parser.add_argument("--step", type=float, default=1.0, help="Sampling step in meters")
    args = parser.parse_args()

    output = args.output or args.input.with_suffix(".osm")
    node_count, way_count, relation_count = build_osm(args.input, output, step=args.step)
    print(
        f"Wrote {output} with {node_count} nodes, {way_count} ways, "
        f"and {relation_count} lanelet relations"
    )


if __name__ == "__main__":
    main()
