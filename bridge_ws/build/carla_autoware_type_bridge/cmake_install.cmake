# Install script for directory: /home/a01004/Desktop/Calra-autoware_interface/bridge_ws/src/carla_autoware_type_bridge

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/install/carla_autoware_type_bridge")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge/vehicle_status_bridge_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge/vehicle_status_bridge_node")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge/vehicle_status_bridge_node"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge" TYPE EXECUTABLE FILES "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/vehicle_status_bridge_node")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge/vehicle_status_bridge_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge/vehicle_status_bridge_node")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge/vehicle_status_bridge_node"
         OLD_RPATH "/opt/ros/humble/lib:/home/a01004/Desktop/Calra-autoware_interface/msg_ws/install/autoware_auto_vehicle_msgs/lib:/home/a01004/autoware/install/autoware_vehicle_msgs/lib:/home/a01004/Desktop/Calra-autoware_interface/msg_ws/install/autoware_auto_planning_msgs/lib:/home/a01004/Desktop/Calra-autoware_interface/msg_ws/install/autoware_auto_geometry_msgs/lib:/home/a01004/Desktop/Calra-autoware_interface/msg_ws/install/autoware_auto_mapping_msgs/lib:/home/a01004/autoware/install/autoware_planning_msgs/lib:/home/a01004/autoware/install/autoware_common_msgs/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge/vehicle_status_bridge_node")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge/control_cmd_bridge_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge/control_cmd_bridge_node")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge/control_cmd_bridge_node"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge" TYPE EXECUTABLE FILES "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/control_cmd_bridge_node")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge/control_cmd_bridge_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge/control_cmd_bridge_node")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge/control_cmd_bridge_node"
         OLD_RPATH "/opt/ros/humble/lib:/home/a01004/Desktop/Calra-autoware_interface/msg_ws/install/autoware_auto_control_msgs/lib:/home/a01004/autoware/install/autoware_control_msgs/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/carla_autoware_type_bridge/control_cmd_bridge_node")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_autoware_type_bridge" TYPE DIRECTORY FILES "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/src/carla_autoware_type_bridge/launch")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/package_run_dependencies" TYPE FILE FILES "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/ament_cmake_index/share/ament_index/resource_index/package_run_dependencies/carla_autoware_type_bridge")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/parent_prefix_path" TYPE FILE FILES "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/ament_cmake_index/share/ament_index/resource_index/parent_prefix_path/carla_autoware_type_bridge")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_autoware_type_bridge/environment" TYPE FILE FILES "/opt/ros/humble/share/ament_cmake_core/cmake/environment_hooks/environment/ament_prefix_path.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_autoware_type_bridge/environment" TYPE FILE FILES "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/ament_cmake_environment_hooks/ament_prefix_path.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_autoware_type_bridge/environment" TYPE FILE FILES "/opt/ros/humble/share/ament_cmake_core/cmake/environment_hooks/environment/path.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_autoware_type_bridge/environment" TYPE FILE FILES "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/ament_cmake_environment_hooks/path.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_autoware_type_bridge" TYPE FILE FILES "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/ament_cmake_environment_hooks/local_setup.bash")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_autoware_type_bridge" TYPE FILE FILES "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/ament_cmake_environment_hooks/local_setup.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_autoware_type_bridge" TYPE FILE FILES "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/ament_cmake_environment_hooks/local_setup.zsh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_autoware_type_bridge" TYPE FILE FILES "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/ament_cmake_environment_hooks/local_setup.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_autoware_type_bridge" TYPE FILE FILES "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/ament_cmake_environment_hooks/package.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/packages" TYPE FILE FILES "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/ament_cmake_index/share/ament_index/resource_index/packages/carla_autoware_type_bridge")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_autoware_type_bridge/cmake" TYPE FILE FILES
    "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/ament_cmake_core/carla_autoware_type_bridgeConfig.cmake"
    "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/ament_cmake_core/carla_autoware_type_bridgeConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_autoware_type_bridge" TYPE FILE FILES "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/src/carla_autoware_type_bridge/package.xml")
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/build/carla_autoware_type_bridge/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
