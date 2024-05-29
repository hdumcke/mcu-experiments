#!/bin/bash

cat > /tmp/sc.yaml << EOF
linux_app:
  agent:
    - source /opt/ros/$ROS_DISTRO/setup.bash
    - source ~/microros_ws/install/local_setup.bash
    - ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888
  node1:
    - source /opt/ros/$ROS_DISTRO/setup.bash
    - source ~/microros_ws/install/local_setup.bash
    - export RMW_IMPLEMENTATION=rmw_microxrcedds
    - ros2 run micro_ros_demos_rclc ping_pong
  node2:
    - source /opt/ros/$ROS_DISTRO/setup.bash
    - source ~/microros_ws/install/local_setup.bash
    - export RMW_IMPLEMENTATION=rmw_microxrcedds
    - ros2 run micro_ros_demos_rclc ping_pong
  node3:
    - source /opt/ros/$ROS_DISTRO/setup.bash
    - source ~/microros_ws/install/local_setup.bash
    - export RMW_IMPLEMENTATION=rmw_microxrcedds
    - ros2 run micro_ros_demos_rclc ping_pong
  node4:
    - source /opt/ros/$ROS_DISTRO/setup.bash
    - source ~/microros_ws/install/local_setup.bash
    - export RMW_IMPLEMENTATION=rmw_microxrcedds
    - ros2 run micro_ros_demos_rclc ping_pong
  viz:
    - source /opt/ros/$ROS_DISTRO/setup.bash
    - sleep 10
    - ros2 topic echo /microROS/ping
EOF

~/.local/bin/screen-commander run /tmp/sc.yaml

# ~/.local/bin/screen-commander kill /tmp/sc.yaml
