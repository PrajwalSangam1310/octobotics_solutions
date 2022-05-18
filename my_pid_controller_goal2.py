#!/usr/bin/env python3

import rospy
from inverted_pendulum_sim.msg import ControlForce, CurrentState
from inverted_pendulum_sim.srv import SetParams
from std_msgs.msg import Float32
import math as m
import numpy as np

pend_applied_force = ControlForce()

length = 300
cart_m = 0.5
pendulum_m = 2

def set_params_client(theta_initial, x_initial):
    print("waiting for service")
    rospy.wait_for_service('/inverted_pendulum/set_params')
    print("found service")
    try:
        set_params = rospy.ServiceProxy('/inverted_pendulum/set_params', SetParams)
        resp1 = set_params(pendulum_m, length, cart_m, \
                        theta_initial,0,0,\
                        x_initial,0,0)
        print(resp1.success, resp1.message)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def publish_force(input_force):
    pend_applied_force.force = input_force
    pub.publish(pend_applied_force.force)

def freq_cb(data):
    freq = data

freq = 0.8
amplitude = 5

if __name__ == "__main__":
    rospy.init_node("pid_controller_inverted_pendulum", anonymous=True)
    set_params_client(0,0)
    # set_params_client(0,0)
    pub = rospy.Publisher("/inverted_pendulum/control_force", ControlForce, queue_size=10)
    sub = rospy.Subscriber("/inverted_pendulum/sin_force_freq", Float32, freq_cb)
    rate = rospy.Rate(100)
    start_time = rospy.get_time()
    
    while not rospy.is_shutdown():
        curr_time = rospy.get_time()
        t = start_time - curr_time
        f  = amplitude*m.sin(2*m.pi*freq*t)
        publish_force(f)
        rate.sleep()