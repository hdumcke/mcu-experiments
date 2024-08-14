#include <stdio.h>
#include <string.h>

#include "motor.h"
#include "robot_parameters.h"

extern struct robot_state_t* robot_state_ptr;
extern struct chassis_t* chassis_ptr;

// PWM interrupt service routine
void on_pwm_wrap() {
//	printf("on_pwm_wrap\n");
    // Clear the interrupt flag that brought us here
    pwm_clear_irq(PWM_SLICE_NUM);
    // Update duty cycle
	if (robot_state_ptr->pwm_change) {
		pwm_set_chan_level(PWM_SLICE_NUM, chassis_ptr->r_motor.pwm_chan, robot_state_ptr->r_pwm);
		pwm_set_chan_level(PWM_SLICE_NUM, chassis_ptr->l_motor.pwm_chan, robot_state_ptr->l_pwm);
		robot_state_ptr->pwm_change = false;
		set_dir_motor(&(chassis_ptr->r_motor), robot_state_ptr->r_dir);
		set_dir_motor(&(chassis_ptr->l_motor), robot_state_ptr->l_dir);
	}
}

void init_motor(struct motor_t *motor, uint8_t gpio_pwm, uint8_t gpio_in1, uint8_t gpio_in2) {
	motor->gpio_pwm = gpio_pwm;
	motor->gpio_in1 = gpio_in1;
	motor->gpio_in2 = gpio_in2;
	motor->pwm_chan = pwm_gpio_to_channel(gpio_pwm);
	gpio_set_function(gpio_pwm, GPIO_FUNC_PWM);
	gpio_init(motor->gpio_in1);
	gpio_init(motor->gpio_in2);
	gpio_set_dir(motor->gpio_in1, GPIO_OUT);
	gpio_set_dir(motor->gpio_in2, GPIO_OUT);
	gpio_put(motor->gpio_in1, 0);
	gpio_put(motor->gpio_in2, 0);
}

void set_dir_motor(struct motor_t *motor, int8_t dir) {
	if (dir > 0) {
		gpio_put(motor->gpio_in1, 0);
		gpio_put(motor->gpio_in2, 1);
	}
	else if (dir < 0) {
		gpio_put(motor->gpio_in1, 1);
		gpio_put(motor->gpio_in2, 0);
	}
	else {
		gpio_put(motor->gpio_in1, 0);
		gpio_put(motor->gpio_in2, 0);
	}
}

void init_chassis(struct chassis_t *chassis) {
	init_motor(&(chassis->r_motor), PWM_OUT+1, R_MOTOR_IN1, R_MOTOR_IN2);
	init_motor(&(chassis->l_motor), PWM_OUT, L_MOTOR_IN1, L_MOTOR_IN2);
	pwm_set_wrap(PWM_SLICE_NUM, WRAPVAL);
    pwm_set_clkdiv(PWM_SLICE_NUM, CLKDIV);
	gpio_init(MOTOR_STDBY);
	gpio_set_dir(MOTOR_STDBY, GPIO_OUT);
	pwm_clear_irq(PWM_SLICE_NUM);
    pwm_set_irq_enabled(PWM_SLICE_NUM, true);
    irq_set_exclusive_handler(PWM_IRQ_WRAP, on_pwm_wrap);
    irq_set_enabled(PWM_IRQ_WRAP, true);
	pwm_set_enabled(PWM_SLICE_NUM, true);
}

void start_chassis(struct chassis_t *chassis) {
	gpio_put(MOTOR_STDBY, 1);
}

void stop_chassis(struct chassis_t *chassis) {
	gpio_put(MOTOR_STDBY, 0);
}
