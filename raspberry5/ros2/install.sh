#!/bin/bash

cd ~
git clone https://github.com/hdumcke/multipass-orchestrator-configurations.git
./multipass-orchestrator-configurations/ubuntu-desktop/build.sh
git clone https://github.com/Tiryoh/ros2_setup_scripts_ubuntu.git
./ros2_setup_scripts_ubuntu/run.sh
source /opt/ros/jazzy/setup.bash

# Create a workspace and download the micro-ROS tools
mkdir microros_ws
cd microros_ws
#git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup
git clone -b rolling https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup

# Update dependencies using rosdep
sudo apt update && rosdep update
rosdep install --from-paths src --ignore-src -y

# Install pip
sudo apt-get install -y python3-pip

# Build micro-ROS tools and source them
colcon build
source install/local_setup.bash
