cmake_minimum_required(VERSION 3.8)
project(carla_autoware_type_bridge)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(autoware_auto_control_msgs REQUIRED)
find_package(autoware_control_msgs REQUIRED)
find_package(autoware_auto_vehicle_msgs REQUIRED)
find_package(autoware_vehicle_msgs REQUIRED)

add_executable(vehicle_status_bridge_node
  src/vehicle_status_bridge_node.cpp)
ament_target_dependencies(vehicle_status_bridge_node
  rclcpp
  autoware_auto_vehicle_msgs
  autoware_vehicle_msgs)

add_executable(control_cmd_bridge_node
  src/control_cmd_bridge_node.cpp)
ament_target_dependencies(control_cmd_bridge_node
  rclcpp
  autoware_auto_control_msgs
  autoware_control_msgs)

install(TARGETS
  vehicle_status_bridge_node
  control_cmd_bridge_node
  DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME})

ament_package()
