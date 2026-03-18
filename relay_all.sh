#!/usr/bin/env bash
set -euo pipefail

# 같은 타입인데 이름만 바꿔서 이어줄 토픽 쌍
# 형식: "입력토픽 출력토픽"
RELAY_PAIRS=(
  "/sensing/lidar/top/pointcloud_before_sync /sensing/lidar/top/pointcloud"
  # "/sensing/lidar/top/pointcloud_before_sync /sensing/lidar/concatenated/pointcloud"
  # "/sensing/lidar/top/pointcloud_before_sync /sensing/lidar/top/pointcloud_raw"
  #"/localization/acceleration /autoware_raw_vehicle_cmd_converter/input/accel"
  #"/system/operation_mode/state /autoware_raw_vehicle_cmd_converter/input/operation_mode_state"
"/localization/acceleration /autoware_raw_vehicle_cmd_converter/input/accel"
"/control/vehicle_cmd_gate/operation_mode /autoware_raw_vehicle_cmd_converter/input/operation_mode_state"
# "/control/vehicle_cmd_gate/operation_mode /autoware_raw_vehicle_cmd_converter/input/operation_mode_state"
"/sensing/imu/tamagawa/imu_raw /sensing/imu/imu_data"
)

PIDS=()

cleanup() {
  echo
  echo "[INFO] stopping relay nodes..."
  for pid in "${PIDS[@]:-}"; do
    kill "$pid" 2>/dev/null || true
  done
}
trap cleanup INT TERM EXIT

idx=0
for pair in "${RELAY_PAIRS[@]}"; do
  read -r input_topic output_topic <<< "$pair"
  node_name="relay_${idx}"

  echo "[START] ${input_topic}  -->  ${output_topic}   (${node_name})"

  if [[ "${input_topic}" == "/sensing/lidar/top/pointcloud_before_sync" ]]; then
    python3 "$(dirname "$0")/pointcloud_relay.py" \
      --input-topic "${input_topic}" \
      --output-topic "${output_topic}" \
      --node-name "${node_name}" &
  elif [[ "${input_topic}" == "/sensing/imu/tamagawa/imu_raw" && "${output_topic}" == "/sensing/imu/imu_data" ]]; then
    python3 "$(dirname "$0")/imu_relay.py" \
      --input-topic "${input_topic}" \
      --output-topic "${output_topic}" \
      --node-name "${node_name}" &
  else
    ros2 run topic_tools relay "${input_topic}" "${output_topic}" \
      --ros-args -r __node:="${node_name}" &
  fi
  PIDS+=("$!")

  idx=$((idx + 1))
done

echo "[INFO] all relays started"
wait
