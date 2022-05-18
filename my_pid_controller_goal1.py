#!/usr/bin/env python3

import rospy
from inverted_pendulum_sim.msg import ControlForce, CurrentState
from inverted_pendulum_sim.srv import SetParams
import math as m
import numpy as np

# this python script calls the service to set the simulation parameters

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

if __name__ == "__main__":
    rospy.init_node("pid_controller_inverted_pendulum", anonymous=True)
    set_params_client(0,0)
    rospy.spin