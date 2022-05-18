# octobotics assignment

## Videos
  - Goal1
    - In the goal1 video file, the script is played which makes the cart_mass, pendulum_mass and the initial x and theta to required values.
  - Goal2
    - The freq and amplitude values are changed and the effects are reflected in graphs.
    - For this rqt_gui plot plugin is used, in that, the gui based on matplotlib is used.
  - Goal3
    - The video shows the working of lqr controller with different initial x values.     

## Tools Used

## Matlab

- Matlab is used to generate the A,B,C,D matrices for the state space modelling. The matlab script is also in the repository.
  - refrences    
- Used the lqr function to generate the K matrix.
- The theta is given more importance than the x value.
- The actuator expenditure is also given less priority than the desired state variables.
- The slx file is also uploaded in the repository.

## Ros

- Ros noetic is used
- Three scripts were created each one for each goal.
- Each scripts solves only for that particular goal.

## Inverted Pendulum solution scripts.
  - goal1_solution.py for goal 1
  - goal2_solution.py for goal 2
  - goal3_solution.py for goal 3

### Goal 1

- The client function is written as per requirement.
- It takes the initial states and sets it with the service call.

### Goal 2

- The script takes the required frequency and amplitude and publishes the sinusoidal force.
- The frequency is kept less than one to see the effect of the force.
- The amplitude is less than 10 so that the pendulum is in the visible window.
- rqt_gui plot plugin is used to display the plots

### Goal 3

- Note: The lqr is designed for cart_mass = 10, pendulum_mass = 10, length = 200, I = 0, b = 0 (as per present in the /src/inverted_pendulum_sim_node.py).
- Script implements the state space controller.
- The k matrix genrated using the matlab.
- The process is simple
  - The subscriber function to the curr_state updates the curr_state in the lqr_controller class.
  - The get_force function gives the force required by taking the dot product of the current state and k_matrix.
- Some manipulation with the curr_state.theta
  - I found that the theta had continuous values i.e, after 2pi the theta didnt start from 0 again, it kept increasing to 4pi and so on.
  - limitted the theta values from 0 to 2pi
  - converted the theta to psi as per the state space requirement.
  - psi = theta - pi
  - this made the domain of theta as -pi to pi
  - this psi was used in later force calculation.
- The calculated force is published on the required topic.    

## Usage

- Place the inverted_pendulum_sim package in the workspace.
- build the package.
- use 
  - `roslaunch inverted_pendulum_sim inverted_pendulum_sim.launch`
- and then
  - `rosrun inverted_pendulum_sim goal3_solution.py`
