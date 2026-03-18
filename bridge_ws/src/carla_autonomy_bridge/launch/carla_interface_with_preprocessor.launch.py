import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(THIS_DIR, "..", "..", "..", ".."))

# Prefer env override; otherwise use workspace-local copy; finally fall back
# to the installed package share.
DEFAULT_AUTOWARE_CARLA_INTERFACE_DIR = os.environ.get(
    "AUTOWARE_CARLA_INTERFACE_SOURCE_DIR"
)
if DEFAULT_AUTOWARE_CARLA_INTERFACE_DIR is None:
    workspace_local_dir = os.path.join(REPO_ROOT, "autoware_carla_interface")
    if os.path.isdir(workspace_local_dir):
        DEFAULT_AUTOWARE_CARLA_INTERFACE_DIR = workspace_local_dir
    else:
        DEFAULT_AUTOWARE_CARLA_INTERFACE_DIR = FindPackageShare(
            "autoware_carla_interface"
        )


def generate_launch_description():
    autoware_carla_interface_dir = LaunchConfiguration(
        "autoware_carla_interface_dir"
    )

    interface_launch = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    autoware_carla_interface_dir,
                    "launch",
                    "autoware_carla_interface.launch.xml",
                ]
            )
        ),
        launch_arguments={
            "host": LaunchConfiguration("host"),
            "port": LaunchConfiguration("port"),
            "timeout": LaunchConfiguration("timeout"),
            "ego_vehicle_role_name": LaunchConfiguration("ego_vehicle_role_name"),
            "vehicle_type": LaunchConfiguration("vehicle_type"),
            "spawn_point": LaunchConfiguration("spawn_point"),
            "carla_map": LaunchConfiguration("carla_map"),
            "sync_mode": LaunchConfiguration("sync_mode"),
            "fixed_delta_seconds": LaunchConfiguration("fixed_delta_seconds"),
            "use_traffic_manager": LaunchConfiguration("use_traffic_manager"),
            "max_real_delta_seconds": LaunchConfiguration("max_real_delta_seconds"),
            "sensor_kit_name": LaunchConfiguration("sensor_kit_name"),
            "sensor_mapping_file": LaunchConfiguration("sensor_mapping_file"),
            "config_file": LaunchConfiguration("config_file"),
        }.items(),
    )

    pointcloud_preprocessor = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("carla_autonomy_bridge"),
                    "launch",
                    "carla_pointcloud_preprocessor.launch.py",
                ]
            )
        ),
        launch_arguments={
            "pointcloud_container_name": LaunchConfiguration("pointcloud_container_name"),
            "vehicle_model": LaunchConfiguration("vehicle_model"),
            "vehicle_mirror_param_file": LaunchConfiguration("vehicle_mirror_param_file"),
            "use_sim_time": LaunchConfiguration("use_sim_time"),
            "use_multithread": LaunchConfiguration("use_multithread"),
            "use_intra_process": LaunchConfiguration("use_intra_process"),
            "crop_box_filter_package": LaunchConfiguration("crop_box_filter_package"),
            "crop_box_filter_plugin": LaunchConfiguration("crop_box_filter_plugin"),
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "autoware_carla_interface_dir",
                default_value=DEFAULT_AUTOWARE_CARLA_INTERFACE_DIR,
                description=(
                    "Path to autoware_carla_interface package "
                    "(env AUTOWARE_CARLA_INTERFACE_SOURCE_DIR overrides)."
                ),
            ),
            DeclareLaunchArgument("host", default_value="localhost"),
            DeclareLaunchArgument("port", default_value="2000"),
            DeclareLaunchArgument("timeout", default_value="20"),
            DeclareLaunchArgument("ego_vehicle_role_name", default_value="ego_vehicle"),
            DeclareLaunchArgument("vehicle_type", default_value="vehicle.tesla.model3"),
            DeclareLaunchArgument("spawn_point", default_value="None"),
            DeclareLaunchArgument("carla_map", default_value="Town01"),
            DeclareLaunchArgument("sync_mode", default_value="True"),
            DeclareLaunchArgument("fixed_delta_seconds", default_value="0.05"),
            DeclareLaunchArgument("use_traffic_manager", default_value="False"),
            DeclareLaunchArgument("max_real_delta_seconds", default_value="0.05"),
            DeclareLaunchArgument(
                "sensor_kit_name", default_value="carla_sensor_kit_description"
            ),
            DeclareLaunchArgument(
                "sensor_mapping_file",
                default_value=PathJoinSubstitution(
                    [
                        autoware_carla_interface_dir,
                        "config",
                        "sensor_mapping.yaml",
                    ]
                ),
            ),
            DeclareLaunchArgument(
                "config_file",
                default_value=PathJoinSubstitution(
                    [
                        autoware_carla_interface_dir,
                        "config",
                        "raw_vehicle_cmd_converter.param.yaml",
                    ]
                ),
            ),
            DeclareLaunchArgument(
                "pointcloud_container_name",
                default_value="/pointcloud_container_for_perception",
            ),
            DeclareLaunchArgument("vehicle_model", default_value="sample_vehicle"),
            DeclareLaunchArgument(
                "vehicle_mirror_param_file",
                default_value="/mnt/hdd/autonomy/.caches/config/vehicle/mirror.param.yaml",
            ),
            DeclareLaunchArgument("use_sim_time", default_value="true"),
            DeclareLaunchArgument("use_multithread", default_value="true"),
            DeclareLaunchArgument("use_intra_process", default_value="true"),
            DeclareLaunchArgument(
                "crop_box_filter_package",
                default_value="pointcloud_preprocessor",
            ),
            DeclareLaunchArgument(
                "crop_box_filter_plugin",
                default_value="pointcloud_preprocessor::CropBoxFilterComponent",
            ),
            interface_launch,
            pointcloud_preprocessor,
        ]
    )
