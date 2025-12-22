---
title: "Lesson 3.3: Programming Basic Movements"
sidebar_position: 3
description: "A hands-on guide to programming fundamental robot motions like moving forward, turning, and stopping, and an introduction to trajectory planning."
tags: [actuators, motion, programming, trajectory, kinematics]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Write code to control a differential drive robot to move forward, backward, and turn.
*   Implement a state machine to sequence multiple movements, like following a square path.
*   Understand the concept of a trajectory and why smooth motion is important.
*   Apply velocity and acceleration limits to a robot's movement.
*   Program a simulated robot to follow a simple, predefined path.

## Prerequisites

*   [Lesson 3.2: Motor Control and PWM](./lesson-02-motor-control-and-pwm.md)

## Theory Section

### From Wheels to Motion

So far, we've learned how to control a single motor. But how do we coordinate multiple motors to achieve purposeful movement? This lesson focuses on programming motion for a common type of mobile robot: a **differential drive robot**.

A differential drive robot has two independently controlled wheels on a common axis. By varying the relative speed of these two wheels, we can control the robot's movement precisely.

*   **Move Forward:** Both wheels spin forward at the same speed.
*   **Move Backward:** Both wheels spin backward at the same speed.
*   **Turn in Place (Right):** The left wheel spins forward, and the right wheel spins backward at the same speed.
*   **Turn in Place (Left):** The right wheel spins forward, and the left wheel spins backward at the same speed.
*   **Curve or Arc:** One wheel spins faster than the other.

![Differential Drive](https://i.imgur.com/8FkP4M4.png)
*Figure 1: How a differential drive robot moves by varying the velocity of its two wheels (V_L and V_R).*

### Sequencing Movements: State Machines

To perform a complex task like navigating a maze or following a path, a robot needs to execute a sequence of simple movements. A **state machine** is a powerful and common programming pattern for managing this.

A state machine consists of:
*   A finite number of **states** (e.g., "MOVING_FORWARD", "TURNING_RIGHT", "STOPPED").
*   **Transitions** between states that are triggered by events (e.g., "target distance reached", "timer expired").

For example, to program a robot to follow a square path, the state machine would look like this:
1.  **State:** `MOVING_FORWARD`. **Action:** Drive both wheels forward. **Transition:** If `distance_traveled >= 1 meter`, switch to state `TURNING_RIGHT`.
2.  **State:** `TURNING_RIGHT`. **Action:** Spin left wheel forward, right wheel backward. **Transition:** If `angle_turned >= 90 degrees`, switch to state `MOVING_FORWARD`.
3.  Repeat four times.
4.  **State:** `STOPPED`.

This is a much cleaner way to program behavior than a single, massive `if/else` block.

### Beyond Basic Movements: Trajectory Planning

Telling a robot to simply "move forward 1 meter" and then "turn 90 degrees" results in jerky, inefficient motion. In the real world, robots (and humans) don't start and stop instantly. They accelerate and decelerate smoothly.

**Trajectory planning** is the process of generating a smooth path (a "trajectory") for a robot to follow between a start point and an end point. A trajectory specifies the robot's desired position, velocity, and acceleration at every point in time.

#### Velocity and Acceleration Limits

A key part of trajectory planning is respecting the physical limits of the robot.
*   **Velocity Limit:** A motor can only spin so fast.
*   **Acceleration Limit:** It takes time to speed up and slow down. A motor can only provide so much torque. Trying to accelerate too quickly can cause wheels to slip or the robot to tip over.

A simple way to create a smoother motion profile is to use a **trapezoidal velocity profile**.
1.  **Accelerate:** Smoothly ramp up the velocity from zero to the maximum allowed speed.
2.  **Cruise:** Maintain a constant maximum velocity.
3.  **Decelerate:** Smoothly ramp down the velocity to zero to arrive at the target position.

This ensures the robot starts and stops smoothly, leading to more stable, predictable, and safer motion.

![Trapezoidal Velocity Profile](https://i.imgur.com/Kx4iXJd.png)
*Figure 2: A trapezoidal velocity profile. The robot accelerates, cruises at a constant velocity, and then decelerates to a stop.*

## Practical Section

In this final lesson of Chapter 3, we will put everything together to program a simulated racecar to follow a square path. We will use a simple state machine to manage the sequence of movements (moving forward and turning).

### The Code

Create a new Python file named `follow_square.py`.

This script defines two main functions: `set_wheel_velocities` to control the robot, and a main loop that implements the state machine. The robot tracks its state (`MOVING_FORWARD` or `TURNING`) and uses timers to decide when to transition to the next state.

```python title="follow_square.py"
import pybullet as p
import time
import pybullet_data

# --- Setup ---
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -10)
p.setRealTimeSimulation(0) # We will manually step the simulation

p.loadURDF("plane.urdf")
car = p.loadURDF("racecar/racecar.urdf", basePosition=[0, 0, 0.2])

# The racecar model has 4 wheel joints (indices 2, 3, 5, 7)
# Let's get the indices for the two rear wheels
# In this model, these are the driven wheels
left_rear_wheel_index = 5
right_rear_wheel_index = 7

# Helper function to set wheel velocities
def set_wheel_velocities(left_velocity, right_velocity):
    """
    Sets the velocity of the two rear wheels.
    """
    p.setJointMotorControl2(
        bodyIndex=car,
        jointIndex=left_rear_wheel_index,
        controlMode=p.VELOCITY_CONTROL,
        targetVelocity=left_velocity,
        force=100
    )
    p.setJointMotorControl2(
        bodyIndex=car,
        jointIndex=right_rear_wheel_index,
        controlMode=p.VELOCITY_CONTROL,
        targetVelocity=right_velocity,
        force=100
    )

# --- State Machine ---
# Define our states
STATE_MOVING_FORWARD = 0
STATE_TURNING = 1

# Initial state
current_state = STATE_MOVING_FORWARD
state_start_time = time.time()
square_side_count = 0

# Parameters for the square path
forward_duration = 2.0  # seconds to drive forward
turn_duration = 1.0     # seconds to turn
wheel_speed = 15        # rad/s

print("Starting to follow a square path...")

try:
    while square_side_count < 4:
        current_time = time.time()
        elapsed_time = current_time - state_start_time

        # --- State Logic ---
        if current_state == STATE_MOVING_FORWARD:
            # Action: Move forward
            set_wheel_velocities(wheel_speed, wheel_speed)

            # Transition: Check if we've moved long enough
            if elapsed_time >= forward_duration:
                print("Finished moving forward, starting turn...")
                current_state = STATE_TURNING
                state_start_time = current_time # Reset timer for the new state
                square_side_count += 1
                if square_side_count == 4:
                    break

        elif current_state == STATE_TURNING:
            # Action: Turn in place (left wheel fwd, right wheel back)
            set_wheel_velocities(wheel_speed, -wheel_speed)

            # Transition: Check if we've turned long enough
            if elapsed_time >= turn_duration:
                print("Finished turning, moving forward...")
                current_state = STATE_MOVING_FORWARD
                state_start_time = current_time # Reset timer

        # Step the simulation
        p.stepSimulation()
        time.sleep(1./240.)

finally:
    print("Finished square path. Stopping.")
    # Stop the robot
    set_wheel_velocities(0, 0)
    # Let it simulate for a moment to see it stop
    for _ in range(100):
        p.stepSimulation()
        time.sleep(1./240.)

    p.disconnect()
```

### Running the Code

Run the script from your terminal: `python follow_square.py`.

You will see the racecar in the simulation window execute the square path maneuver. It will:
1.  Drive forward for 2 seconds.
2.  Turn in place for 1 second.
3.  Repeat this sequence four times.
4.  Stop.

You have successfully programmed a basic motion sequence!

## Self-Assessment

1.  On a differential drive robot, how would you make it execute a wide right turn?
2.  What is the purpose of a state machine in robotics programming?
3.  What is a "trajectory" in the context of robotics?
4.  Why is a trapezoidal velocity profile better than a simple "on/off" (square) velocity profile?
5.  In the code example, how is the "state" of the robot being tracked?

---

**Answer Key:**

1.  To make a wide right turn, you would make the left wheel spin faster than the right wheel. Both wheels would still be spinning forward.
2.  A state machine provides a structured way to manage and sequence a robot's behaviors, making the code easier to write, debug, and understand.
3.  A trajectory is a path that specifies the robot's desired position, velocity, and acceleration over time.
4.  A trapezoidal profile ensures smooth acceleration and deceleration, which is more stable, predictable, and less stressful on the robot's mechanical components.
5.  The state is tracked using the `current_state` variable, which holds a value like `STATE_MOVING_FORWARD` or `STATE_TURNING`.

## Further Reading

*   [Introduction to State Machines](https://www.youtube.com/watch?v=E_J2gOKGv1s) - A good conceptual overview.
*   [Kinematics of Differential Drive Robots](http://www.cs.columbia.edu/~allen/F17/NOTES/icckinematics.pdf) - A more in-depth look at the math behind the motion.
*   [Trajectory Planning for Robot Manipulators](https://www.youtube.com/watch?v=1p_a2h5n4no) - A video from a Northwestern Robotics course that introduces the concepts visually.
