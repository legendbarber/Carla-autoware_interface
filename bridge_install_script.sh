BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE_DIR/msg_ws"
colcon build --symlink-install

source "$BASE_DIR/msg_ws/install/setup.bash"

cd "$BASE_DIR/bridge_ws"
colcon build \
  --packages-select carla_autoware_type_bridge carla_autonomy_bridge \
  --cmake-clean-cache \
  --cmake-args \
  -Dautoware_auto_vehicle_msgs_DIR="$BASE_DIR/msg_ws/install/autoware_auto_vehicle_msgs/share/autoware_auto_vehicle_msgs/cmake"

cd "$BASE_DIR/autoware_carla_interface"
colcon build --symlink-install --packages-select autoware_carla_interface
source "$BASE_DIR/autoware_carla_interface/install/setup.bash"

cd "$BASE_DIR"

echo "Build done."
echo "Run these before launching:"
echo "source $BASE_DIR/msg_ws/install/setup.bash"
echo "source $BASE_DIR/bridge_ws/install/setup.bash"
echo "source $BASE_DIR/autoware_carla_interface/install/setup.bash"
