# carla_autonomy_bridge

CARLA <-> Autoware 브릿지용 보조 패키지입니다.
`carla_autoware_type_bridge` 실행과 함께 필요한 토픽 relays 및
포인트클라우드 전처리 런치를 묶어둡니다.

## 포함 내용
- `relays.launch.py`: 기존 `relay_all.sh`를 ROS 2 launch로 패키지화
- `bridge_with_relays.launch.py`: `carla_autoware_type_bridge/bridges.launch.py` + relays 동시 실행
- `carla_interface_with_preprocessor.launch.py`: CARLA 인터페이스 + 포인트클라우드 전처리
- `carla_pointcloud_preprocessor.launch.py`: 포인트클라우드 전처리만 실행
- `pointcloud_relay`, `imu_relay` 커스텀 노드

## 사용 방법 (다른 사람 기준)
1) 이 폴더를 ROS 2 워크스페이스의 `src`로 복사/클론

2) 빌드
```bash
cd ~/bridge_ws
colcon build --packages-select carla_autonomy_bridge
source install/setup.bash
```

3) 실행
- 기존 `ros2 launch carla_autoware_type_bridge bridges.launch.py` + `relay_all.sh` 조합:
```bash
ros2 launch carla_autonomy_bridge bridge_with_relays.launch.py
```

- relays만 실행:
```bash
ros2 launch carla_autonomy_bridge relays.launch.py
```

- CARLA 인터페이스 + 포인트클라우드 전처리:
```bash
ros2 launch carla_autonomy_bridge carla_interface_with_preprocessor.launch.py
```

## 환경 변수
- `AUTOWARE_CARLA_INTERFACE_SOURCE_DIR`
  - 기본값: 워크스페이스 루트의 `autoware_carla_interface/`가 있으면 그 경로 사용
  - 없으면 설치된 `autoware_carla_interface` 패키지 share 경로 사용
- `AUTONOMY_CONFIG_DIR`
  - 기본값: `/mnt/hdd/autonomy/.caches/config`

## 주의 사항
- `carla_autoware_type_bridge` 패키지가 설치되어 있어야 합니다.
- `topic_tools`, `pointcloud_preprocessor`, `autoware_global_parameter_loader`에 의존합니다.
- 메시지 라이브러리 경로 문제가 있으면 아래처럼 `LD_LIBRARY_PATH`를 잡아주세요:
```bash
export LD_LIBRARY_PATH=~/msg_ws/install/autoware_auto_vehicle_msgs/lib:$LD_LIBRARY_PATH
```
