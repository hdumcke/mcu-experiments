#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "hardware/gpio.h"
#include "hardware/pwm.h"
#include "pico/stdlib.h"
#include "pico/multicore.h"

#include "bt_hid.h"
#include "robot_parameters.h"
#include "motor.h"

#define TESTING false

struct robot_state_t robot_state;
struct robot_state_t* robot_state_ptr = &robot_state;
struct chassis_t chassis;
struct chassis_t* chassis_ptr = &chassis;

static inline int8_t clamp8(int16_t value) {
        if (value > 127) {
                return 127;
        } else if (value < -127) {
                return -127;
        }

        return value;
}

static inline int16_t clamp_pwm(int16_t value) {
        if (value > PWM_MAX) return PWM_MAX;

        return value;
}

static inline float scale_cmd_vel(int8_t value, float max_val) {
	if (value != 0) return value * max_val / 127;
	else return 0.0;
}

#define EPSILON 0.001
static inline int16_t scale_pwm(float value, int16_t min_val, int16_t max_val) {
	if ((value > -EPSILON) && (value < EPSILON)) return 0.0;
	return min_val + value * max_val / VX_MAX;
}

void main(void) {
	stdio_init_all();
	init_robot(robot_state_ptr);
	init_chassis(chassis_ptr);
	start_chassis(chassis_ptr);

	sleep_ms(1000);
	printf("Hello\n");

	multicore_launch_core1(bt_main);
	// Wait for init (should do a handshake with the fifo here?)
	sleep_ms(1000);

	if (TESTING) {
	// testing
	robot_state.l_pwm = 300;
	robot_state.l_dir = -1;
	robot_state.r_pwm = 300;
	robot_state.r_dir = -1;
	robot_state.pwm_change = true;
	sleep_ms(20);
	}


	struct bt_hid_state state;
	for ( ;; ) {
		sleep_ms(20);
		bt_hid_get_latest(&state);

		int8_t linear = clamp8(-(state.ly - 128));
		int8_t rot = clamp8(-(state.rx - 128));
		if (!TESTING) {
			float vx = scale_cmd_vel(linear, VX_MAX);
			float vw = scale_cmd_vel(rot, VZ_MAX);
			float vr = (vx + vw * BASE_WIDTH / 2.0);
			float vl = (vx - vw * BASE_WIDTH / 2.0);
			int16_t r_pwm = scale_pwm(vr, PWM_MIN, PWM_MAX);
			int16_t l_pwm = scale_pwm(vl, PWM_MIN, PWM_MAX);
			printf("linear %.4f rot %.4f r_pwm %d l_pwm %d\n", vx, vw, r_pwm, l_pwm);
			int8_t l_dir = 0;
			int8_t r_dir = 0;
			if (l_pwm > 0) l_dir = 1;
			if (l_pwm < 0) l_dir = -1;
			if (r_pwm > 0) r_dir = 1;
			if (r_pwm < 0) r_dir = -1;
			l_pwm = clamp_pwm(abs(l_pwm));
			r_pwm = clamp_pwm(abs(r_pwm));
			bool pwm_change = false;
			if (l_pwm != robot_state.l_pwm) {
				pwm_change = true;
				robot_state.l_pwm = l_pwm;
			}
			if (r_pwm != robot_state.r_pwm) {
				pwm_change = true;
				robot_state.r_pwm = r_pwm;
			}
			if (l_dir != robot_state.l_dir) {
				pwm_change = true;
				robot_state.l_dir = l_dir;
			}
			if (r_dir != robot_state.r_dir) {
				pwm_change = true;
				robot_state.r_dir = r_dir;
			}
			robot_state.pwm_change = pwm_change;
		}


	}
}
