# mcu-experiments

This is a playground for me to better understand how to program MCUs and how to apply best practices for software development.

As a bare minimum the SW development process must work from CLI for further automation and must integrate well with git. The goal is to use CI and to have good test coverage to a certain extend. Since embedded SW is time critical limitations are expected.

## Platforms under test

This is based on the platforms I have readily available:

- STM32: Nucleo development board with F446RE
- ESP32: ESP-WROOM-32
- Teensy 4.1
- RP2040: Raspberry Pi Pico H and WH
- Arduino UNO

## Methodology

- Research: Collect basic information and write document
- Define use cases
- Document suggest development environments for each platform
- Identify CLI workflow
- Identify libraries
- Research test tools

## Real Time OS

Research what is available.

Test FreeRTOS 

## Virtualisation

QUEMU

## Robotics Use Case

Develop a wheeled platform with wheel encoders, implement SW on different HW platforms, study portability, develop and test CI approach.

## Micro Python

Test micro python with C++ bindings

## Micro ROS

Test micro-ROS

# Status

very early stage
