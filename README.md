# octobotics assignment
Inverted Pendulum solution scripts.
  - goal1_solution.py for goal 1
  - goal2_solution.py for goal 2
  - goal3_solution.py for goal 3

## Tools Used

## Matlab

- Matlab is used to generate the A,B,C,D matrices for the state space modelling. The matlab script is also in the repository.
  - refrences    
- Used the lqr function to generate the K matrix.
- The theta is given more importance than the x value.
- The actuator expenditure is also given less priority than the desired state variables.
- The slx file is also uploaded in the repository.

## Ros

- Three scripts were created each one for each goal.
- Each scripts solves only for that particular goal.

### Goal 1

- The client function is written as per requirement.
- It takes the initial states and sets it with the service call.

### Goal 2

- The script takes the required frequency and amplitude and publishes the sinusoidal force.
- The frequency is kept less than one to see the effect of the force.
- The amplitude is less than 10 so that the pendulum is in the visible window.
- rqt_gui plot plugin is used to display the plots

### Goal 3

- Script implements the state space controller.
- The k matrix genrated using the matlab is used in here.
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
