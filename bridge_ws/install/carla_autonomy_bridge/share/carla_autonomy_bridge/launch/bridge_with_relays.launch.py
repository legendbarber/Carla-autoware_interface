from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    carla_bridge = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("carla_autoware_type_bridge"),
                    "launch",
                    "bridges.launch.py",
                ]
            )
        )
    )

    relays = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("carla_autonomy_bridge"),
                    "launch",
                    "relays.launch.py",
                ]
            )
        )
    )

    return LaunchDescription([carla_bridge, relays])
