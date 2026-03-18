BASE_DIR="$(pwd)"
cd "$BASE_DIR/msg_ws"
colcon build --symlink-install

source "$BASE_DIR/msg_ws/install/setup.bash"

cd "$BASE_DIR/bridge_ws"
colcon build \
  --packages-select carla_autoware_type_bridge carla_autonomy_bridge \
  --cmake-clean-cache \
  --cmake-args \
  -Dautoware_auto_vehicle_msgs_DIR="$BASE_DIR/msg_ws/install/autoware_auto_vehicle_msgs/share/autoware_auto_vehicle_msgs/cmake"

cd "$BASE_DIR"