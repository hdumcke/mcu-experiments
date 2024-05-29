# ROS2 on Raspberry Pi 4

Base OS: Ubuntu 22.04 (jammy)
ROS2 Distribution: Humble Hawksbill (humble)

## Installation

Prepare SD card with Ubuntu 22.04 Dektop using the Raspberry Pi Imager

```
./prepare_sd.py
```

## Demo

Build the demo with 

```
./build_example_linux.sh
```

Run the demo with

```
./run_example_linux.sh
```

This will create a detached screen session. To connect:

```
screen -r
```
