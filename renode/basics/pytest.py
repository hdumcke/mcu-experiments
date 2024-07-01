#!/usr/bin/env python3

from pyrenode import connect_renode, get_keywords, shutdown_renode

uart = 'sysbus.usart0'

connect_renode()
get_keywords()

ExecuteCommand('i @nrf52_adafruit_feather.resc')
CreateTerminalTester(uart)
ExecuteCommand(f"showAnalyzer {uart}")

StartEmulation()
WaitForPromptOnUart("uart:~")
WriteLineToUart("version")
WaitForLineOnUart("Zephyr* version 1.14.0-rc1", timeout=60, treatAsRegex=True)

print(ExecuteCommand('echo "Test passed!"'))

shutdown_renode()
