#!/bin/bash

source /opt/ros/humble/setup.bash
source ~/microros_ws/install/local_setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyAMA1 -b 1000000
#TODO write lauunch file
