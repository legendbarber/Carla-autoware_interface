## 토픽 브릿지 관련
### 1. 브릿지 설치 스크립트
bash bridge_install_script.sh

### 2. 브릿지 실행명령어(총 2개 있음)
source "$(pwd)/bridge_ws/install/setup.bash"
export LD_LIBRARY_PATH="$(pwd)/msg_ws/install/autoware_auto_vehicle_msgs/lib:$LD_LIBRARY_PATH"
ros2 launch carla_autoware_type_bridge bridges.launch.py

chmod +x relay_all.sh
./relay_all.sh

### 3. carla-autoware interface실행 
1. 실행전 interface코드 수정 불필요
이 워크스페이스에 `autoware_carla_interface/`를 포함해 두었고, 런치에서 자동으로 이 경로를 사용함.
다른 PC로 옮겨도 해당 폴더만 같이 가져가면 됨.
필요하면 아래 중 하나로 경로를 덮어쓸 수 있음.
- 환경변수: `AUTOWARE_CARLA_INTERFACE_SOURCE_DIR`
- 런치 인자: `autoware_carla_interface_dir:=/path/to/autoware_carla_interface`

2. carla-autoware interface실행 명령어
ros2 launch carla_interface_with_preprocessor.launch.py

---
## autoware모듈 관련
: 각 모듈에서 바뀐 파라미터들을 정리해놓음(빌드안하고 사용할거면 install에서만 바꿔도됨)

### 1. control: 
- run.sh : use_sim_time:=false -> true. 
- mpc.param.yaml, lateral_controller_defaults.param.yaml : admissible_position_error 5.0 -> 10.0, admissible_yaw_error_rad 1.57 -> 2.20. 
- pid.param.yaml : enable_large_tracking_error_emergency true -> false.


### 2. localization:
- ekf_localizer.param.yaml : predict_frequency 50.0 -> 10.0, tf_rate 50.0 -> 10.0
- ndt_scan_matcher.param.yaml : use_dynamic_map_loading true -> false, max_iterations 30 -> 60, converged_param_nearest_voxel_transformation_likelihood 2.3 -> 0.3.
      
### 3. map: 
- 맵 파일만 잘 넣어준다
[furive-map]AW-SampleMap_v1.0.0_ws/install/autoware_launch/share/autoware_launch/config/map


---

## CARLA, CARLA-autoware interface, 브릿지 코드 실행 예시
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
```
