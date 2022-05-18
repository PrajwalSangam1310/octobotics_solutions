#!/usr/bin/env python3

import rospy
from inverted_pendulum_sim.msg import ControlForce, CurrentState
from inverted_pendulum_sim.srv import SetParams
import math as m
import numpy as np

pend_current_state = CurrentState()
pend_applied_force = ControlForce()

length = 200
cart_m = 10
pendulum_m = 10

class LQR_controller:
    def __init__(self):
        self.K = [0,0,0,0]
        
        self.cur_state = [0,0,0,0] #x, x_dot, theta, theta_dot

    def update_k(self, K):
        for i in range(len(self.K)):
            self.K[i] = K[i]

    def update_state(self, state):
        for i in range(len(state)):
            self.cur_state[i] = state[i]

    def get_force(self):
        return -(self.K[0]*(self.cur_state[0]) + self.K[1]*self.cur_state[1] + self.K[2]*(self.cur_state[2]) + self.K[3]*self.cur_state[3])
        
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

def state_callback(data):
    pend_current_state.curr_x = data.curr_x
    pend_current_state.curr_x_dot = data.curr_x_dot
    pend_current_state.curr_x_dot_dot = data.curr_x_dot_dot

    # to convert the continuous rotation to 0, 2*pi
    pend_current_state.curr_theta = data.curr_theta - data.curr_theta//(2*m.pi)
    # convert the theta to phi as per in the state space analysis, angle phi is considered from positive y axis, whereas theta is from negative y axis.
    pend_current_state.curr_theta = pend_current_state.curr_theta - m.pi
    
    #debugging
    print("theta",pend_current_state.curr_theta, "theta_dot", pend_current_state.curr_theta_dot)
    pend_current_state.curr_theta_dot = data.curr_theta_dot
    pend_current_state.curr_theta_dot_dot = data.curr_theta_dot_dot
    my_controller.update_state([pend_current_state.curr_x, pend_current_state.curr_x_dot, pend_current_state.curr_theta, pend_current_state.curr_theta_dot])

def publish_force():
    pend_applied_force.force = my_controller.get_force()
    pub.publish(pend_applied_force.force)

#controller parameters
# LQR
# r = 0.01
# Q = [1 0 0 0;
#      0 1 0 0;
#      0 0 10 0; preference for theta correction
#      0 0 0 1]
my_controller = LQR_controller()
K = np.array([-0.0003 ,  -0.0037   , 0.2358   , 1.0199])*10000
my_controller.update_k(K)

if __name__ == "__main__":
    rospy.init_node("pid_controller_inverted_pendulum", anonymous=True)
    #initial parameters with 10 degrees and -200 as x coordinate
    set_params_client(m.pi - m.radians(10),-200)
    # set_params_client(0,0)
    pub = rospy.Publisher("/inverted_pendulum/control_force", ControlForce, queue_size=10)
    sub = rospy.Subscriber("/inverted_pendulum/current_state", CurrentState, state_callback)
    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
        publish_force()
        rate.sleep()
