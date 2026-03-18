#include <memory>
#include <string>
#include <functional>

#include "rclcpp/rclcpp.hpp"
#include "autoware_vehicle_msgs/msg/gear_report.hpp"
#include "autoware_vehicle_msgs/msg/velocity_report.hpp"
#include "autoware_vehicle_msgs/msg/steering_report.hpp"
#include "autoware_vehicle_msgs/msg/control_mode_report.hpp"
#include "autoware_auto_vehicle_msgs/msg/gear_report.hpp"
#include "autoware_auto_vehicle_msgs/msg/velocity_report.hpp"
#include "autoware_auto_vehicle_msgs/msg/steering_report.hpp"
#include "autoware_auto_vehicle_msgs/msg/control_mode_report.hpp"

class VehicleStatusBridgeNode : public rclcpp::Node
{
public:
  VehicleStatusBridgeNode()
  : Node("vehicle_status_bridge_node")
  {
    gear_input_topic_ = declare_parameter<std::string>(
      "gear_input_topic", "/vehicle/status/gear_status");
    gear_output_topic_ = declare_parameter<std::string>(
      "gear_output_topic", "/vehicle/status/gear_status");

    velocity_input_topic_ = declare_parameter<std::string>(
      "velocity_input_topic", "/vehicle/status/velocity_status");
    velocity_output_topic_ = declare_parameter<std::string>(
      "velocity_output_topic", "/vehicle/status/velocity_status");

    steering_input_topic_ = declare_parameter<std::string>(
      "steering_input_topic", "/vehicle/status/steering_status");
    steering_output_topic_ = declare_parameter<std::string>(
      "steering_output_topic", "/vehicle/status/steering_status");

    control_mode_input_topic_ = declare_parameter<std::string>(
      "control_mode_input_topic", "/vehicle/status/control_mode");
    control_mode_output_topic_ = declare_parameter<std::string>(
      "control_mode_output_topic", "/vehicle/status/control_mode");

    const auto qos = rclcpp::QoS(rclcpp::KeepLast(1)).reliable();

    gear_pub_ = create_publisher<autoware_auto_vehicle_msgs::msg::GearReport>(
      gear_output_topic_, qos);
    velocity_pub_ = create_publisher<autoware_auto_vehicle_msgs::msg::VelocityReport>(
      velocity_output_topic_, qos);
    steering_pub_ = create_publisher<autoware_auto_vehicle_msgs::msg::SteeringReport>(
      steering_output_topic_, qos);
    control_mode_pub_ = create_publisher<autoware_auto_vehicle_msgs::msg::ControlModeReport>(
      control_mode_output_topic_, qos);

    gear_sub_ = create_subscription<autoware_vehicle_msgs::msg::GearReport>(
      gear_input_topic_, qos,
      std::bind(&VehicleStatusBridgeNode::on_gear, this, std::placeholders::_1));

    velocity_sub_ = create_subscription<autoware_vehicle_msgs::msg::VelocityReport>(
      velocity_input_topic_, qos,
      std::bind(&VehicleStatusBridgeNode::on_velocity, this, std::placeholders::_1));

    steering_sub_ = create_subscription<autoware_vehicle_msgs::msg::SteeringReport>(
      steering_input_topic_, qos,
      std::bind(&VehicleStatusBridgeNode::on_steering, this, std::placeholders::_1));

    control_mode_sub_ = create_subscription<autoware_vehicle_msgs::msg::ControlModeReport>(
      control_mode_input_topic_, qos,
      std::bind(&VehicleStatusBridgeNode::on_control_mode, this, std::placeholders::_1));

    RCLCPP_INFO(get_logger(), "Vehicle status bridges enabled.");
    RCLCPP_INFO(get_logger(), "  gear         : %s -> %s", gear_input_topic_.c_str(), gear_output_topic_.c_str());
    RCLCPP_INFO(get_logger(), "  velocity     : %s -> %s", velocity_input_topic_.c_str(), velocity_output_topic_.c_str());
    RCLCPP_INFO(get_logger(), "  steering     : %s -> %s", steering_input_topic_.c_str(), steering_output_topic_.c_str());
    RCLCPP_INFO(get_logger(), "  control_mode : %s -> %s", control_mode_input_topic_.c_str(), control_mode_output_topic_.c_str());
  }

private:
  void on_gear(const autoware_vehicle_msgs::msg::GearReport::SharedPtr msg)
  {
    autoware_auto_vehicle_msgs::msg::GearReport out{};
    out.stamp = msg->stamp;
    out.report = msg->report;
    gear_pub_->publish(out);
  }

  void on_velocity(const autoware_vehicle_msgs::msg::VelocityReport::SharedPtr msg)
  {
    autoware_auto_vehicle_msgs::msg::VelocityReport out{};
    out.header = msg->header;
    out.longitudinal_velocity = msg->longitudinal_velocity;
    out.lateral_velocity = msg->lateral_velocity;
    out.heading_rate = msg->heading_rate;
    velocity_pub_->publish(out);
  }

  void on_steering(const autoware_vehicle_msgs::msg::SteeringReport::SharedPtr msg)
  {
    autoware_auto_vehicle_msgs::msg::SteeringReport out{};
    out.stamp = msg->stamp;
    out.steering_tire_angle = msg->steering_tire_angle;
    steering_pub_->publish(out);
  }

  void on_control_mode(const autoware_vehicle_msgs::msg::ControlModeReport::SharedPtr msg)
  {
    autoware_auto_vehicle_msgs::msg::ControlModeReport out{};
    out.stamp = msg->stamp;
    out.mode = msg->mode;
    control_mode_pub_->publish(out);
  }

  std::string gear_input_topic_;
  std::string gear_output_topic_;
  std::string velocity_input_topic_;
  std::string velocity_output_topic_;
  std::string steering_input_topic_;
  std::string steering_output_topic_;
  std::string control_mode_input_topic_;
  std::string control_mode_output_topic_;

  rclcpp::Subscription<autoware_vehicle_msgs::msg::GearReport>::SharedPtr gear_sub_;
  rclcpp::Subscription<autoware_vehicle_msgs::msg::VelocityReport>::SharedPtr velocity_sub_;
  rclcpp::Subscription<autoware_vehicle_msgs::msg::SteeringReport>::SharedPtr steering_sub_;
  rclcpp::Subscription<autoware_vehicle_msgs::msg::ControlModeReport>::SharedPtr control_mode_sub_;

  rclcpp::Publisher<autoware_auto_vehicle_msgs::msg::GearReport>::SharedPtr gear_pub_;
  rclcpp::Publisher<autoware_auto_vehicle_msgs::msg::VelocityReport>::SharedPtr velocity_pub_;
  rclcpp::Publisher<autoware_auto_vehicle_msgs::msg::SteeringReport>::SharedPtr steering_pub_;
  rclcpp::Publisher<autoware_auto_vehicle_msgs::msg::ControlModeReport>::SharedPtr control_mode_pub_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<VehicleStatusBridgeNode>());
  rclcpp::shutdown();
  return 0;
}
