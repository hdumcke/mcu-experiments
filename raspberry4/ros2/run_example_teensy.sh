#!/bin/bash

cat > /tmp/test_cdm.sh << EOF
#!/bin/bash

source /opt/ros/$ROS_DISTRO/setup.bash
ros2 topic pub --once /microROS/ping std_msgs/msg/Header '{frame_id: "fake_ping"}'
EOF
chmod +x /tmp/test_cdm.sh

cat > /tmp/sc.yaml << EOF
linux_app:
  agent:
    - source /opt/ros/$ROS_DISTRO/setup.bash
    - source ~/microros_ws/install/local_setup.bash
    - ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0
  viz:
    - source /opt/ros/$ROS_DISTRO/setup.bash
    - sleep 8
    - ros2 topic echo /microROS/ping
  test:
    - echo run /tmp/test_cdm.sh
EOF

~/.local/bin/screen-commander run /tmp/sc.yaml

# ~/.local/bin/screen-commander kill /tmp/sc.yaml
