#include <cstdio>
#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include <string.h>
#include <sstream>
#include "rclcpp/rclcpp.hpp"

#include "irobot_create_msgs/msg/wheel_ticks.hpp"

class Odom : public rclcpp::Node
{
public:
	Odom():Node("odom")
	{
		odom_subscriber_=
			this->create_subscription<irobot_create_msgs::msg::WheelTicks>(
			"/wheel_ticks",
			rclcpp::SensorDataQoS(),
			std::bind(&Odom::wheel_ticks_callback,this,std::placeholders::_1));
	}
private:
	void wheel_ticks_callback(
		const irobot_create_msgs::msg::WheelTicks::SharedPtr wheel_ticks)
	{
		std::stringstream strs;
		char* char_type;
		strs<<wheel_ticks->ticks_left;
		char_type = (char*) (strs.str()).c_str();
		RCLCPP_INFO(this->get_logger(),"Ticks Left:");
		RCLCPP_INFO(this->get_logger(),char_type);
		strs<<wheel_ticks->ticks_right;
                char_type = (char*) (strs.str()).c_str();
		RCLCPP_INFO(this->get_logger(),"Ticks Right:");
                RCLCPP_INFO(this->get_logger(),char_type);

	}
	rclcpp::Subscription<irobot_create_msgs::msg::WheelTicks>::SharedPtr odom_subscriber_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Odom>());
  rclcpp::shutdown();

  return 0;
}
