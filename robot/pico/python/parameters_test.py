import asyncio
from parameters import RobotParameters, ParamServer
from time import ticks_ms

params = RobotParameters("192.168.1.32")
server = ParamServer(params)
last_called = ticks_ms()


async def show_cmd_vel(params):
    global last_called
    while True:
        now = ticks_ms()
        if (now - last_called) > 100:
            last_called = now
            params.tele_plot.send_value("vx", params.robot_params['cmd_vel']['value'][0])
            params.tele_plot.send_value("vy", params.robot_params['cmd_vel']['value'][1])
            params.tele_plot.send_value("vz", params.robot_params['cmd_vel']['value'][2])
        await asyncio.sleep_ms(100)


async def main(server, params):
    asyncio.create_task(server.serve())
    asyncio.create_task(show_cmd_vel(params))
    while True:
        await asyncio.sleep_ms(10_000)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(server, params))
