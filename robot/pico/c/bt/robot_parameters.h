#include "pico/stdlib.h"

#define M_PI 3.14159265358979323846

#define VX_MAX 0.7f
#define VZ_MAX 1.0f * M_PI

#define PWM_MIN 300
#define PWM_MAX 5000

#define WHEEL_DIAMETER 0.0336  // wheel diameter [m]
#define BASE_WIDTH 0.116       // wheel width [m]

struct robot_state_t {
	float l_rpm; 
	float r_rpm;
	int16_t l_pwm; 
	int16_t r_pwm;
	int8_t l_dir; 
	int8_t r_dir;
	bool pwm_change;
};

void init_robot(struct robot_state_t *state);
