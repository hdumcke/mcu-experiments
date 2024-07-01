# Micro-ROS2 on Raspberry Pi 4

Base OS: Ubuntu 22.04 (jammy)
ROS2 Distribution: Humble Hawksbill (humble)

## Installation

Prepare SD card with Ubuntu 22.04 Server using the Raspberry Pi Imager. Mount SD on PC and run

```
./prepare_sd.py
```

Once the Sd card is prepared boot Raspberry Pi 4 off this card. Cloud-init will configure the Wifi network and the user password. Copy this repo to the Raspberry Pi and execute 

```
./build.sh
```

## Check Status

```
sudo systemctl status micro-ros
ros2 node list
ros2 topic list
```
