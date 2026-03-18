from setuptools import setup

package_name = "carla_autonomy_bridge"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (
            f"share/{package_name}/launch",
            [
                "launch/relays.launch.py",
                "launch/bridge_with_relays.launch.py",
                "launch/carla_interface_with_preprocessor.launch.py",
                "launch/carla_pointcloud_preprocessor.launch.py",
            ],
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="a01004",
    maintainer_email="a01004@local",
    description="CARLA <-> Autoware bridge helpers and relays",
    license="Proprietary",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "pointcloud_relay = carla_autonomy_bridge.pointcloud_relay:main",
            "imu_relay = carla_autonomy_bridge.imu_relay:main",
        ]
    },
)
