from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    relay_pairs = [
        # (input_topic, output_topic, kind)
        (
            "/sensing/lidar/top/pointcloud_before_sync",
            "/sensing/lidar/top/pointcloud",
            "pointcloud",
        ),
        (
            "/localization/acceleration",
            "/autoware_raw_vehicle_cmd_converter/input/accel",
            "topic_tools",
        ),
        (
            "/control/vehicle_cmd_gate/operation_mode",
            "/autoware_raw_vehicle_cmd_converter/input/operation_mode_state",
            "topic_tools",
        ),
        (
            "/sensing/imu/tamagawa/imu_raw",
            "/sensing/imu/imu_data",
            "imu",
        ),
    ]

    nodes = []
    for idx, (input_topic, output_topic, kind) in enumerate(relay_pairs):
        node_name = f"relay_{idx}"
        if kind == "pointcloud":
            nodes.append(
                Node(
                    package="carla_autonomy_bridge",
                    executable="pointcloud_relay",
                    arguments=[
                        "--input-topic",
                        input_topic,
                        "--output-topic",
                        output_topic,
                        "--node-name",
                        node_name,
                    ],
                    output="screen",
                )
            )
        elif kind == "imu":
            nodes.append(
                Node(
                    package="carla_autonomy_bridge",
                    executable="imu_relay",
                    arguments=[
                        "--input-topic",
                        input_topic,
                        "--output-topic",
                        output_topic,
                        "--node-name",
                        node_name,
                    ],
                    output="screen",
                )
            )
        else:
            nodes.append(
                Node(
                    package="topic_tools",
                    executable="relay",
                    name=node_name,
                    arguments=[input_topic, output_topic],
                    output="screen",
                )
            )

    return LaunchDescription(nodes)
