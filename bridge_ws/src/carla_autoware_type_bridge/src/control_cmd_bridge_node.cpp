#include <memory>
#include <string>
#include <functional>

#include "rclcpp/rclcpp.hpp"
#include "autoware_auto_control_msgs/msg/ackermann_control_command.hpp"
#include "autoware_control_msgs/msg/control.hpp"

class ControlCmdBridgeNode : public rclcpp::Node
{
public:
  ControlCmdBridgeNode()
  : Node("control_cmd_bridge_node")
  {
    input_topic_ = declare_parameter<std::string>(
      "input_topic", "/control/command/control_cmd");
    output_topic_ = declare_parameter<std::string>(
      "output_topic", "/control/command/control_cmd");

    const auto qos = rclcpp::QoS(rclcpp::KeepLast(1)).reliable();

    pub_ = create_publisher<autoware_control_msgs::msg::Control>(output_topic_, qos);
    sub_ = create_subscription<autoware_auto_control_msgs::msg::AckermannControlCommand>(
      input_topic_, qos,
      std::bind(&ControlCmdBridgeNode::on_msg, this, std::placeholders::_1));

    RCLCPP_INFO(
      get_logger(), "Control command bridge enabled: %s -> %s",
      input_topic_.c_str(), output_topic_.c_str());
  }

private:
  void on_msg(const autoware_auto_control_msgs::msg::AckermannControlCommand::SharedPtr msg)
  {
    autoware_control_msgs::msg::Control out{};

    out.stamp = msg->stamp;
    out.control_time = msg->stamp;

    out.lateral.stamp = msg->stamp;
    out.lateral.control_time = msg->stamp;
    out.lateral.steering_tire_angle = msg->lateral.steering_tire_angle;
    out.lateral.steering_tire_rotation_rate = msg->lateral.steering_tire_rotation_rate;
    out.lateral.is_defined_steering_tire_rotation_rate = true;

    out.longitudinal.stamp = msg->stamp;
    out.longitudinal.control_time = msg->stamp;
    out.longitudinal.velocity = msg->longitudinal.speed;
    out.longitudinal.acceleration = msg->longitudinal.acceleration;
    out.longitudinal.jerk = msg->longitudinal.jerk;
    out.longitudinal.is_defined_acceleration = true;
    out.longitudinal.is_defined_jerk = true;

    pub_->publish(out);
  }

  std::string input_topic_;
  std::string output_topic_;

  rclcpp::Subscription<autoware_auto_control_msgs::msg::AckermannControlCommand>::SharedPtr sub_;
  rclcpp::Publisher<autoware_control_msgs::msg::Control>::SharedPtr pub_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ControlCmdBridgeNode>());
  rclcpp::shutdown();
  return 0;
}
