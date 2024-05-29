micro-ROS
=========

https://micro.ros.org

.. code-block:: bash

   # install ROS2 Humble on Ubuntu 22.04
   # Source the ROS 2 installation
   source /opt/ros/$ROS_DISTRO/setup.bash

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
   
   # Create firmware step
   ros2 run micro_ros_setup create_firmware_ws.sh host
   
   # Build step
   ros2 run micro_ros_setup build_firmware.sh
   source install/local_setup.bash
   
   # Download micro-ROS-Agent packages
   ros2 run micro_ros_setup create_agent_ws.sh
   
   # Build step
   ros2 run micro_ros_setup build_agent.sh
   source install/local_setup.bash
   
   # Run a micro-ROS agent
   ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888
   
   #  in another command line, run the micro-ROS node 
   source /opt/ros/$ROS_DISTRO/setup.bash
   source ~/microros_ws/install/local_setup.bash

   # Use RMW Micro XRCE-DDS implementation
   export RMW_IMPLEMENTATION=rmw_microxrcedds

   # Run a micro-ROS node
   ros2 run micro_ros_demos_rclc ping_pong
   
   #  in another command line, test the micro-ROS app
   source /opt/ros/$ROS_DISTRO/setup.bash

   # Subscribe to micro-ROS ping topic
   ros2 topic echo /microROS/ping
