#include "robot_parameters.h"

void init_robot(struct robot_state_t *state)
  {
      state->l_rpm = 0.0;
      state->r_rpm = 0.0;
      state->l_pwm = 0;
      state->r_pwm = 0;
      state->l_dir = 0;
      state->r_dir = 0;
	  state->pwm_change = false;
  }
