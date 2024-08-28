class FeedForward:
    def __init__(self, threshold, bias, Kp, Kd):
        self.threshold = threshold
        self.bias = bias
        self.Kp = Kp
        self.Kd = Kd
        self.last_setpoint = 0.0

    def reset(self):
        self.last_setpoint = 0.0

    def process(self, setpoint):
        derivative = setpoint - self.last_setpoint
        self.last_setpoint = setpoint
        setpoint_abs = abs(setpoint)
        setpoint_sign = 0
        if setpoint_abs > self.threshold:
            setpoint_sign = setpoint_abs / setpoint
            bias_term = setpoint_sign * self.bias
        else:
            bias_term = 0.0
        p_term = self.Kp * (setpoint - setpoint_sign * self.threshold)
        d_term = self.Kd * derivative

        return bias_term + p_term + d_term
