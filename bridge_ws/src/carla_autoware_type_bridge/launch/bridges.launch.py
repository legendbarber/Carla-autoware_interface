from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='carla_autoware_type_bridge',
            executable='vehicle_status_bridge_node',
            name='vehicle_status_bridge_node',
            output='screen',
            parameters=[{
                'gear_input_topic': '/vehicle/status/gear_status',
                'gear_output_topic': '/vehicle/status/gear_status',
                'velocity_input_topic': '/vehicle/status/velocity_status',
                'velocity_output_topic': '/vehicle/status/velocity_status',
                'steering_input_topic': '/vehicle/status/steering_status',
                'steering_output_topic': '/vehicle/status/steering_status',
                'control_mode_input_topic': '/vehicle/status/control_mode',
                'control_mode_output_topic': '/vehicle/status/control_mode',
            }],
        ),
        Node(
            package='carla_autoware_type_bridge',
            executable='control_cmd_bridge_node',
            name='control_cmd_bridge_node',
            output='screen',
            parameters=[{
                'input_topic': '/control/command/control_cmd',
                'output_topic': '/control/command/control_cmd2',
            }],
        ),
    ])
