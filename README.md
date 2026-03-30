## 1. 브릿지 패키지 설치 스크립트
bash bridge_install_script.sh


---

## 2. autoware모듈 파라미터 세팅
: 각 모듈에서 바뀐 파라미터들을 정리해놓음(빌드안하고 사용할거면 아마도 install에서만 바꿔도됨. 혹시 심링크 걸려있는게 잇을수있으니 src에서도 바꾸는걸 추천)

### 1. control: 
- run.sh : use_sim_time:=false -> true. 
- mpc.param.yaml, lateral_controller_defaults.param.yaml : admissible_position_error 5.0 -> 10.0, admissible_yaw_error_rad 1.57 -> 2.20. 
- pid.param.yaml : enable_large_tracking_error_emergency true -> false.

### 2. localization:
- ekf_localizer.param.yaml : predict_frequency 50.0 -> 10.0, tf_rate 50.0 -> 10.0
- ndt_scan_matcher.param.yaml : use_dynamic_map_loading true -> false, max_iterations 30 -> 60, converged_param_nearest_voxel_transformation_likelihood 2.3 -> 0.3.
      
### 3. map: 
- 맵 파일(lanelet2_map.osm, pointcloud_map.pcd, map_projector_info.yaml)만 잘 넣어준다
[furive-map]AW-SampleMap_v1.0.0_ws/install/autoware_launch/share/autoware_launch/config/map

### 4. gui:
- run.sh : use_sim_time:=false -> true

### 5. perception :
- run.sh : use_sim_time:=false -> true, lidar_detection_model:=clustering

### 6. planning : 
- run.sh : use_sim_time:=true
- obstacle_avoidance_planner.param.yaml : enable_warm_start true -> false 
- mpt_optimizer.cpp : updateL/updateU 호출 2개가 있던 거를 , updateBounds(lower_bound, upper_bound)로 합쳐준다

### 7. system
- run.sh : use_sim_time:=false -> true, launch_system_monitor:=true -> false. 

### 8. vehicle
- run.sh : launch_vehicle_interface:=true use_sim_time:=true
- sensor_kit_calibration.yaml : velodyne_top_base_link.yaw 1.575 -> 0
- /path/to/vehicle_module/install/sample_vehicle_description/share/sample_vehicle_description/config/* : sensors_calibration.yaml파일, sensor_kit_calibration.yaml파일 각 커스텀 센서 재원에 맞게 수정 -> '4. 차량 재원 참고 레퍼런스' 참고
- /path/to/vehicle_module/install/individual_params/share/individual_params/config/default/sample_sensor_kit/* : vehicle_info.param.yaml파일, mirror.param.yaml파일 차량 재원에 맞게 수정 -> '4. 차량 재원 참고 레퍼런스' 참고

---

## 3. CARLA, CARLA-autoware interface, 브릿지 코드 실행
```bash
# terminal 1 : carla실행
cd /path/to/carla
./CarlaUE4.sh

# terminal 2 : carla-autoware interface 실행
cd /path/to/Carla-autoware_interface
ros2 launch carla_interface_with_preprocessor.launch.py

# terminal 3 : 첫번째 브릿지(변환) 코드 실행
cd /path/to/Carla-autoware_interface
source "$(pwd)/bridge_ws/install/setup.bash"
export LD_LIBRARY_PATH="$(pwd)/msg_ws/install/autoware_auto_vehicle_msgs/lib:$LD_LIBRARY_PATH"
ros2 launch carla_autoware_type_bridge bridges.launch.py

# terminal 4 : 두번째 브릿지(릴레이) 코드 실행
cd /path/to/Carla-autoware_interface
chmod +x relay_all.sh
./relay_all.sh

# terminal 5 : autoware모듈 8개 실행
# control, gui, localization, samplemap, perception, planning, system, samplevehicle
```


### 코드들 실행전에 확인사항
: 브릿지가 실행되는 각 터미널에서 확실히
```bash
source $BASE_DIR/msg_ws/install/setup.bash
source $BASE_DIR/bridge_ws/install/setup.bash
source $BASE_DIR/autoware_carla_interface/install/setup.bash
```
위 명령어로 변수를 세팅해줘야한다. 또한 브릿지 코드에는 따로 에러로그가 안나오기 때문에
```bash
# interface쪽 주요 토픽
ros2 topic info /control/command/actuation_cmd
ros2 topic info /sensing/lidar/top/pointcloud_before_sync 
ros2 topic info /vehicle/status/actuation_status

# autoware쪽 주요 토픽
ros2 topic info /control/command/control_cmd
ros2 topic info /control/command/control_cmd2
ros2 topic info /sensing/lidar/top/pointcloud
ros2 topic info /sensing/lidar/concatenated/pointcloud
```
위와 같은 명령어로 브릿지 코드실행후, 제대로 연결되고 있는지 확인해야한다.

---
## 4. 차량 재원 참고 레퍼런스
1. vehicle_info.param.yaml
```yaml
/**:
  ros__parameters:
    wheel_radius: 0.122 # The radius of the wheel, primarily used for dead reckoning.
    wheel_width: 0.065 # The lateral width of a wheel tire, primarily used for dead reckoning.
    wheel_base: 0.60 # between front wheel center and rear wheel center
    wheel_tread: 0.52 # between left wheel center and right wheel center
    front_overhang: 0.12 # between front wheel center and vehicle front
    rear_overhang: 0.15 # between rear wheel center and vehicle rear
    left_overhang: 0.05 # between left wheel center and vehicle left
    right_overhang: 0.05 # between right wheel center and vehicle right
    vehicle_height: 0.60
    max_steer_angle: 0.70 # [rad]
```
2. mirror.param.yaml
```yaml
/**:
  ros__parameters:
    min_longitudinal_offset: 0.0
    max_longitudinal_offset: 0.0
    min_lateral_offset: 0.0
    max_lateral_offset: 0.0
    min_height_offset: 0.0
    max_height_offset: 0.0
```
3. sensors_calibration.yaml
```yaml
base_link:
  sensor_kit_base_link:
    x: 0.0
    y: 0.0
    z: 0.0
    roll: 0.0
    pitch: 0.0
    yaw: 0.0
  velodyne_rear_base_link:
    x: 0.0
    y: 0.0
    z: 0.0
    roll: 0.0
    pitch: 0.0
    yaw: 0.0
```
4. sensor_kit_calibration.yaml
```yaml
sensor_kit_base_link:
  camera0/camera_link:
    x: 0.10731
    y: 0.56343
    z: -0.27697
    roll: -0.025
    pitch: 0.315
    yaw: 1.035
  camera1/camera_link:
    x: -0.10731
    y: -0.56343
    z: -0.27697
    roll: -0.025
    pitch: 0.32
    yaw: -2.12
  camera2/camera_link:
    x: 0.10731
    y: -0.56343
    z: -0.27697
    roll: -0.00
    pitch: 0.335
    yaw: -1.04
  camera3/camera_link:
    x: -0.10731
    y: 0.56343
    z: -0.27697
    roll: 0.0
    pitch: 0.325
    yaw: 2.0943951
  camera4/camera_link:
    x: 0.07356
    y: 0.0
    z: -0.0525
    roll: 0.0
    pitch: -0.03
    yaw: -0.005
  camera5/camera_link:
    x: -0.07356
    y: 0.0
    z: -0.0525
    roll: 0.0
    pitch: -0.01
    yaw: 3.125
  traffic_light_right_camera/camera_link:
    x: 0.05
    y: -0.0175
    z: -0.1
    roll: 0.0
    pitch: 0.0
    yaw: 0.0
  traffic_light_left_camera/camera_link:
    x: 0.05
    y: 0.0175
    z: -0.1
    roll: 0.0
    pitch: 0.0
    yaw: 0.0
  velodyne_top_base_link:
    x: 0.100
    y: 0.000
    z: 0.600
    roll: 0.000
    pitch: 0.000
    yaw: 0.000
  velodyne_left_base_link:
    x: 0.0
    y: 0.56362
    z: -0.30555
    roll: -0.02
    pitch: 0.71
    yaw: 1.575
  velodyne_right_base_link:
    x: 0.0
    y: -0.56362
    z: -0.30555
    roll: -0.01
    pitch: 0.71
    yaw: -1.580
  gnss_link:
    x: 0.000
    y: 0.000
    z: 1.200
    roll: 0.000
    pitch: 0.000
    yaw: 0.000
  tamagawa/imu_link:
    x: 0.000
    y: 0.000
    z: 0.500
    roll: 0.000
    pitch: 0.000
    yaw: 0.000
```
