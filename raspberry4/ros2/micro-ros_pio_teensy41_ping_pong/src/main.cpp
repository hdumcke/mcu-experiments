#include <Arduino.h>
#include <micro_ros_platformio.h>

#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

#include <std_msgs/msg/header.h>

#include <stdio.h>
#include <unistd.h>
#include <time.h>

#define STRING_BUFFER_LEN 100

rcl_publisher_t ping_publisher;
rcl_publisher_t pong_publisher;
rcl_subscription_t ping_subscriber;
rcl_subscription_t pong_subscriber;

std_msgs__msg__Header incoming_ping;
std_msgs__msg__Header outcoming_ping;
std_msgs__msg__Header incoming_pong;

char outcoming_ping_buffer[STRING_BUFFER_LEN];
char incoming_ping_buffer[STRING_BUFFER_LEN];
char incoming_pong_buffer[STRING_BUFFER_LEN];

rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

int device_id;
int seq_no;
int pong_count;

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}

// Error handle loop
void error_loop() {
  while(1) {
    delay(100);
  }
}

void ping_timer_callback(rcl_timer_t * timer, int64_t last_call_time)
{
	RCLC_UNUSED(last_call_time);

	if (timer != NULL) {

		seq_no = random(1000);
		sprintf(outcoming_ping.frame_id.data, "%d_%d", seq_no, device_id);
		outcoming_ping.frame_id.size = strlen(outcoming_ping.frame_id.data);
		
		// Fill the message timestamp
		unsigned long last_time { millis() };
		outcoming_ping.stamp.sec = int(last_time / 10);
		outcoming_ping.stamp.nanosec = last_time * 10;

		// Reset the pong count and publish the ping message
		pong_count = 0;
		RCSOFTCHECK(rcl_publish(&ping_publisher, (const void*)&outcoming_ping, NULL));
	}
}

void ping_subscription_callback(const void * msgin)
{
	const std_msgs__msg__Header * msg = (const std_msgs__msg__Header *)msgin;

	// Dont pong my own pings
	if(strcmp(outcoming_ping.frame_id.data, msg->frame_id.data) != 0){
		RCSOFTCHECK(rcl_publish(&pong_publisher, (const void*)msg, NULL));
	}
}


void pong_subscription_callback(const void * msgin)
{
	const std_msgs__msg__Header * msg = (const std_msgs__msg__Header *)msgin;

	if(strcmp(outcoming_ping.frame_id.data, msg->frame_id.data) == 0) {
			pong_count++;
	}
}

void setup() {
  // Configure serial transport
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();

  //create init_options
  RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

  // create node
  RCCHECK(rclc_node_init_default(&node, "pingpong_node", "", &support));

  // create ping publisher
  RCCHECK(rclc_publisher_init_default(
    &ping_publisher,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Header),
    "/microROS/ping"));

  // create pong publisher
  RCCHECK(rclc_publisher_init_best_effort(
    &pong_publisher,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Header),
    "/microROS/pong"));

  // create ping subscriber
  RCCHECK(rclc_subscription_init_best_effort(
    &ping_subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Header),
    "/microROS/ping"));

  // create pong subscriber
  RCCHECK(rclc_subscription_init_best_effort(
    &pong_subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Header),
    "/microROS/pong"));

  // create timer,
  const unsigned int timer_timeout = 2000;
  RCCHECK(rclc_timer_init_default(
    &timer,
    &support,
    RCL_MS_TO_NS(timer_timeout),
    ping_timer_callback));

  // Create executor
  RCCHECK(rclc_executor_init(&executor, &support.context, 3, &allocator));
  RCCHECK(rclc_executor_add_timer(&executor, &timer));
  RCCHECK(rclc_executor_add_subscription(&executor, &ping_subscriber, &incoming_ping, &ping_subscription_callback, ON_NEW_DATA));
  RCCHECK(rclc_executor_add_subscription(&executor, &pong_subscriber, &incoming_pong, &pong_subscription_callback, ON_NEW_DATA));

  // Create and allocate the pingpong messages

  outcoming_ping.frame_id.data = outcoming_ping_buffer;
  outcoming_ping.frame_id.capacity = STRING_BUFFER_LEN;

  incoming_ping.frame_id.data = incoming_ping_buffer;
  incoming_ping.frame_id.capacity = STRING_BUFFER_LEN;

  incoming_pong.frame_id.data = incoming_pong_buffer;
  incoming_pong.frame_id.capacity = STRING_BUFFER_LEN;

  randomSeed(analogRead(0));
  device_id = random(1000);

}

void loop() {
  delay(100);
  RCSOFTCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100)));
}
