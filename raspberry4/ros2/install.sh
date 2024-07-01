#!/bin/bash

cd ~
git clone https://github.com/Tiryoh/ros2_setup_scripts_ubuntu.git
sed -i "s/CHOOSE_ROS_DISTRO=jazzy/CHOOSE_ROS_DISTRO=humble/" ./ros2_setup_scripts_ubuntu/run.sh
sed -i "s/INSTALL_PACKAGE=desktop/INSTALL_PACKAGE=ros-base/" ./ros2_setup_scripts_ubuntu/run.sh
./ros2_setup_scripts_ubuntu/run.sh
source /opt/ros/humble/setup.bash

# Create a workspace and download the micro-ROS tools
mkdir microros_ws
cd microros_ws
git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup

# Update dependencies using rosdep
sudo apt update && rosdep update
rosdep install --from-paths src --ignore-src -y

# Install pip
sudo apt-get install -y python3-pip

# Build micro-ROS tools and source them
colcon build
source install/local_setup.bash

# Download micro-ROS-Agent packages
ros2 run micro_ros_setup create_agent_ws.sh
