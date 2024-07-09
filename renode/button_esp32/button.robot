*** Variables ***
${LED}                          sysbus.gpioa.greenled2

*** Test Cases ***
button on esp32
    ${x}=                       Execute Command         include @${CURDIR}/button.resc
    Create Terminal Tester      sysbus.usart2    timeout=15
    Create LED Tester           ${LED}

    Wait For Line On Uart       *** Booting Zephyr OS build v3.7.0-rc1-339-g243783243cbd ***

    Wait For Line On Uart       Set up button at gpio@40020800 pin 13
    Wait For Line On Uart       Set up LED at gpio@40020000 pin 5    
    Wait For Prompt On Uart     Press the button
    Assert LED State            true
    Execute Command             emulation PauseAll
    Execute Command             gpioc.button Press
    Execute Command             emulation RunFor "0.1"
    Assert LED State            false
    Execute Command             gpioc.button Release
    Execute Command             emulation RunFor "0.1"
    Assert LED State            true
