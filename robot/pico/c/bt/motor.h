#include "pico/stdlib.h"
#include "hardware/pwm.h"
#include "hardware/gpio.h"
#include "hardware/irq.h"

// PWM wrap value and clock divide value
// For a CPU rate of 125 MHz, this gives
// a PWM frequency of 1 kHz.
#define WRAPVAL 5000
#define CLKDIV 25.0f

// we use GPIO 10 and 11 for PWM
// We wnt to use the same slice so that we have a common interupt routine
#define PWM_OUT 10
#define PWM_SLICE_NUM 5

#define L_MOTOR_IN1 13
#define L_MOTOR_IN2 12
#define R_MOTOR_IN1 15
#define R_MOTOR_IN2 14
#define MOTOR_STDBY 20

struct motor_t {
    uint8_t gpio_pwm;
    uint8_t pwm_chan;
    uint8_t gpio_in1;
    uint8_t gpio_in2;
};

void init_motor(struct motor_t *motor, uint8_t gpio_pwm, uint8_t gpio_in1, uint8_t gpio_in2);
void set_dir_motor(struct motor_t *motor, int8_t dir);

struct chassis_t {
    struct motor_t r_motor;
    struct motor_t l_motor;
};

void init_chassis(struct chassis_t *chassis);
void start_chassis(struct chassis_t *chassis);
void stop_chassis(struct chassis_t *chassis);


// PWM interrupt service routine
void on_pwm_wrap();
