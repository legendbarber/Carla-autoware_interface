#!/usr/bin/env python3

import argparse

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from rclpy.qos import DurabilityPolicy
from rclpy.qos import HistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import ReliabilityPolicy
from sensor_msgs.msg import Imu


class ImuRelay(Node):
    def __init__(self, input_topic: str, output_topic: str, node_name: str) -> None:
        super().__init__(node_name)

        qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
        )

        self._publisher = self.create_publisher(Imu, output_topic, qos)
        self._subscription = self.create_subscription(
            Imu,
            input_topic,
            self._on_msg,
            qos,
        )

        self.get_logger().info(
            f"IMU relay enabled: {input_topic} -> {output_topic}"
        )

    def _on_msg(self, msg: Imu) -> None:
        self._publisher.publish(msg)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-topic", required=True)
    parser.add_argument("--output-topic", required=True)
    parser.add_argument("--node-name", default="imu_relay")
    args = parser.parse_args()

    rclpy.init()
    node = ImuRelay(args.input_topic, args.output_topic, args.node_name)

    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
