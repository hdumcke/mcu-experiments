*** Variables ***
${LED}                          sysbus.gpio0.led0

*** Test Cases ***
blinky on rpi_pico
    ${x}=                       Execute Command         include @${CURDIR}/blinky.resc
    Create Terminal Tester      sysbus.uart0    timeout=15
    Create LED Tester           ${LED}

    Wait For Line On Uart       *** Booting Zephyr OS build af57038bb053 ***    pauseEmulation=true
    Wait For Line On Uart       LED state: (ON|OFF)      treatAsRegex=true            pauseEmulation=true
    Assert LED Is Blinking      testDuration=4  onDuration=1  offDuration=1           pauseEmulation=true