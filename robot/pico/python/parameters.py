import socket
import network
import select
import asyncio
from time import time, ticks_ms


class TelePlot:
    def __init__(self, target):
        self.teleplot_target = target
        self.teleplot_port = 47269
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

    def send_value(self, name, value, unit=None, flags=None):
        a = "%s:%s:%s" % (name, ticks_ms(), value)
        if unit:
            a = "%s§%s" % (a, unit)
        if flags:
            a = "%s|%s" % (a, flags)
        self.s.sendto(a.encode('utf-8'), (self.teleplot_target, self.teleplot_port))

    def send_values_xy(self, name, values):
        a = "%s:%s:%s:%s|xy" % (name, values[0], values[1], ticks_ms())
        self.s.sendto(a.encode('utf-8'), (self.teleplot_target, self.teleplot_port))


class RobotParameters:
    def __init__(self, target):
        self.robot_params = {}
        self.init_params()
        self.tele_plot = TelePlot(target)

    def init_params(self):
        self.add_param('float_test', 'float', 2)
        self.add_param('bool_test', 'bool', 2)
        self.add_param('int_test', 'int', 2)
        self.add_param('str_test', 'str', 2)

        self.add_param('cmd_vel', 'float', 3)
        self.add_param('robot_pose', 'float', 3)
        self.add_param('robot_vel', 'float', 3)
        self.add_param('robot_acc', 'float', 3)
        self.add_param('encoder_speed', 'float', 2)

    def add_param(self, name, param_type, length):
        self.robot_params[name] = {}
        self.robot_params[name]['timestamp'] = time()
        if param_type == 'float':
            self.robot_params[name]['type'] = self.cvt_float
            self.update_param(name, [0.0] * length)
        if param_type == 'bool':
            self.robot_params[name]['type'] = self.cvt_bool
            self.update_param(name, [False] * length)
        if param_type == 'int':
            self.robot_params[name]['type'] = self.cvt_int
            self.update_param(name, [0] * length)
        if param_type == 'str':
            self.robot_params[name]['type'] = self.cvt_str
            self.update_param(name, [''] * length)
        self.robot_params["show_%s" % name] = {}
        self.robot_params["show_%s" % name]['timestamp'] = time()
        self.robot_params["show_%s" % name]['value'] = [False]

    def update_param(self, name, value):
        self.robot_params[name]['value'] = value
        self.robot_params[name]['timestamp'] = time()

    def cvt_int(self, s):
        return int(s)

    def cvt_float(self, s):
        return float(s)

    def cvt_bool(self, s):
        return s == "True"

    def cvt_str(self, s):
        return s

    def show_params(self):
        for param in self.robot_params:
            if param[0:4] == "show" and self.robot_params[param]['value'][0]:
                for i in range(len(self.robot_params[param[5:]]['value'])):
                    self.tele_plot.send_value("%s_%i", param[5:], self.robot_params[param[5:]]['value'][i])


class ParamServer:
    def __init__(self, params):
        self.params = params
        udp_port = 8080
        wlan = network.WLAN(network.STA_IF)
        ip = wlan.ifconfig()[0]
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.s.setblocking(False)
        self.s.bind((ip, udp_port))

    async def serve(self):
        p = select.poll()
        p.register(self.s, select.POLLIN)
        while True:
            try:
                if p.poll(1):
                    buf, addr = self.s.recvfrom(1024)
                    cmd = buf.decode('utf-8').strip().split(':')
                    if cmd[0] in self.params.robot_params.keys():
                        for i in range(len(cmd[1:])):
                            self.params.robot_params[cmd[0]]['value'][i] = self.params.robot_params[cmd[0]]['type'](cmd[i + 1])
                await asyncio.sleep(0)
            except asyncio.core.CancelledError:
                self.s.close()
                return
