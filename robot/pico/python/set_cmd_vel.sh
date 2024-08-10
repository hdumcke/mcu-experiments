#!/bin/bash

echo "cmd_vel:0.0:0.0:0.0" | nc -u -w0  192.168.1.67 8080
