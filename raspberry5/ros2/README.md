# ROS2 on Raspberry Pi 5

Base OS: Ubuntu 24.04 (Noble)
ROS2 Distribution: Jazzy Jalisco (jazzy)

## Installation

Prepare SD card with Ubuntu 24.04 Dektop using the Raspberry Pi Imager

TODO: check cloud-init
for now install manually.

```
sudo apt install -y openssh-server
echo "$USER ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/$USER
sudo chmod 640 /etc/sudoers.d/$USER
sudo apt install -y git python-is-python3
```
