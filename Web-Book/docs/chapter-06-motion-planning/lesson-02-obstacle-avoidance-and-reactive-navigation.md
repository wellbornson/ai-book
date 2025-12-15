--- 
title: "Lesson 6.2: Obstacle Avoidance and Reactive Navigation"
sidebar_position: 2
description: "Explore how robots react to unexpected obstacles using methods like potential fields and bug algorithms, and understand the interplay between global and local planning."
tags: [obstacle-avoidance, reactive-navigation, potential-fields, local-planning, dynamic-obstacles]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Differentiate between global (path) planning and local (reactive) planning.
*   Explain the concept of Artificial Potential Fields for obstacle avoidance.
*   Describe how a robot uses potential fields to navigate towards a goal and avoid obstacles.
*   Understand the advantages and limitations of reactive navigation strategies.
*   Implement a simple potential field-based obstacle avoidance system in PyBullet.

## Prerequisites

*   [Lesson 6.1: Grid-Based Path Planning](./lesson-01-grid-based-path-planning.md)

## Theory Section

### The Gap Between Plan and Reality

In the previous lesson, we learned about A* for **global path planning** – finding an optimal path from start to goal in a known, static map. However, the real world is rarely perfectly known or static. What happens if an unexpected obstacle appears, or if the robot deviates from its planned path?

This is where **local planning** or **reactive navigation** comes in. Reactive methods enable robots to respond immediately to sensor readings to avoid collisions, often without explicit knowledge of a global map or a predefined path.

### Global vs. Local Planning

It's crucial to understand the distinction:

*   **Global Planning (Path Planning):**
    *   **Goal:** Find an optimal path from start to goal through a *known* environment.
    *   **Information:** Requires a complete map of the environment.
    *   **Output:** A sequence of waypoints or a full trajectory.
    *   **Example:** A* algorithm.
    *   **Limitations:** Cannot handle unexpected obstacles; computationally intensive to re-plan frequently.

*   **Local Planning (Reactive Navigation / Obstacle Avoidance):**
    *   **Goal:** Avoid immediate collisions and reach a local objective (e.g., move towards the global path).
    *   **Information:** Uses immediate sensor readings (e.g., proximity sensors, LiDAR, depth cameras).
    *   **Output:** Immediate motor commands (e.g., turn left, slow down).
    *   **Example:** Potential fields, Bug algorithms.
    *   **Limitations:** Can get stuck in local minima; may not find the optimal path globally.

Most successful robotic systems combine both: a global planner calculates a coarse path, and a local reactive layer handles immediate obstacle avoidance and unexpected situations.

### Artificial Potential Fields

The **Artificial Potential Field** method is a popular reactive navigation technique inspired by physics. Imagine the robot as a charged particle, the goal as an attractive force, and obstacles as repulsive forces.

*   **Attractive Field:** The goal creates an attractive force, pulling the robot towards it. The force increases as the robot gets farther from the goal.
*   **Repulsive Field:** Each obstacle creates a repulsive force, pushing the robot away. The force is stronger the closer the robot gets to the obstacle.

The robot then calculates the **resultant force (vector sum)** from all attractive and repulsive fields. It moves in the direction of this resultant force.

    ![Artificial Potential Fields](https://i.imgur.com/nJ2kR3B.png)
    *Figure 1: The robot is attracted to the goal (G) and repelled by obstacles. The sum of these forces dictates its movement.*

*   **Advantages:** Simple to implement, generates smooth paths, computationally efficient, good for dynamic obstacle avoidance.
*   **Limitations:** Can get stuck in **local minima** (e.g., a "valley" between obstacles that isn't the goal, or oscillations if attractive and repulsive forces perfectly balance). Cannot navigate through narrow passages.

### Bug Algorithms

**Bug algorithms** are another class of reactive navigation methods that enable a robot to circumnavigate obstacles. They are guaranteed to find a path to the goal if one exists.

*   **How it works (simplified):** The robot typically tries to move directly towards the goal. If it hits an obstacle, it follows the boundary of the obstacle until it can once again move directly towards the goal. Different "bug" algorithms have different rules for when to leave the obstacle boundary.
*   **Advantages:** Simple, guaranteed to find a path (if one exists), no map needed.
*   **Limitations:** Can generate very long, inefficient paths; often requires contact with the obstacle.

## Practical Section

In this exercise, we will implement a simple Artificial Potential Field method in PyBullet. Our simulated robot will try to reach a target while being repelled by nearby obstacles.

### The Code

Create a new file named `potential_fields.py`.

We'll load our `racecar` robot and place several cube obstacles. We'll define a target position for the robot. In the main loop, the robot will calculate an attractive force towards the target and repulsive forces from each obstacle (simulated using proximity to the robot's base). The sum of these forces will determine the robot's linear and angular velocity commands.

```python title="potential_fields.py"
import pybullet as p
import time
import pybullet_data
import math
import numpy as np

# --- Robot Parameters ---
WHEEL_RADIUS = 0.1
WHEEL_BASE = 0.5

# --- Potential Field Parameters ---
ATTRACTIVE_GAIN = 0.5 # Kp for attractive force
REPULSIVE_GAIN = 0.5 # Kp for repulsive force
OBSTACLE_RADIUS = 0.5 # Distance at which obstacles start repelling
MAX_VELOCITY = 10.0 # rad/s for wheels
MAX_LINEAR_VEL = 0.5 # m/s
MAX_ANGULAR_VEL = 1.0 # rad/s

# --- Setup ---
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -10)
p.setRealTimeSimulation(0)

p.loadURDF("plane.urdf")
car = p.loadURDF("racecar/racecar.urdf", basePosition=[0, 0, 0.1])
# Initial robot pose for visualization
robot_pos, robot_ori = p.getBasePositionAndOrientation(car)
robot_pose = np.array([robot_pos[0], robot_pos[1], p.getEulerFromQuaternion(robot_ori)[2]])

# The racecar model has 4 wheel joints (indices 2, 3, 5, 7)
left_rear_wheel_index = 5
right_rear_wheel_index = 7

# Place some obstacles
obstacles = []
obstacles.append(p.loadURDF("cube_small.urdf", basePosition=[2, 0.5, 0.5]))
obstacles.append(p.loadURDF("cube_small.urdf", basePosition=[2, -0.5, 0.5]))
obstacles.append(p.loadURDF("cube_small.urdf", basePosition=[3, 0, 0.5]))
obstacles.append(p.loadURDF("sphere_small.urdf", basePosition=[1.0, 1.0, 0.5]))

# Define the target goal
goal_position = np.array([5.0, 0.0])

# --- Control Functions ---
def set_differential_drive_velocities(v_linear, omega_angular):
    v_left = (v_linear - (omega_angular * WHEEL_BASE / 2))
    v_right = (v_linear + (omega_angular * WHEEL_BASE / 2))

    target_left_ang_vel = np.clip(v_left / WHEEL_RADIUS, -MAX_VELOCITY, MAX_VELOCITY)
    target_right_ang_vel = np.clip(v_right / WHEEL_RADIUS, -MAX_VELOCITY, MAX_VELOCITY)

    p.setJointMotorControl2(
        bodyIndex=car,
        jointIndex=left_rear_wheel_index,
        controlMode=p.VELOCITY_CONTROL,
        targetVelocity=target_left_ang_vel,
        force=100
    )
    p.setJointMotorControl2(
        bodyIndex=car,
        jointIndex=right_rear_wheel_index,
        controlMode=p.VELOCITY_CONTROL,
        targetVelocity=target_right_ang_vel,
        force=100
    )

# --- Main Loop ---
time_step = 1.0/240.0
print("Starting Potential Fields Navigation...")

try:
    while True:
        robot_pos_xyz, robot_ori_xyzw = p.getBasePositionAndOrientation(car)
        robot_current_x = robot_pos_xyz[0]
        robot_current_y = robot_pos_xyz[1]
        robot_current_yaw = p.getEulerFromQuaternion(robot_ori_xyzw)[2]
        
        current_robot_position = np.array([robot_current_x, robot_current_y])

        # 1. Calculate Attractive Force
        vector_to_goal = goal_position - current_robot_position
        distance_to_goal = np.linalg.norm(vector_to_goal)
        
        attractive_force = ATTRACTIVE_GAIN * vector_to_goal # Proportional to distance
        
        # 2. Calculate Repulsive Force from each obstacle
        total_repulsive_force = np.array([0.0, 0.0])
        for obs_id in obstacles:
            obs_pos_xyz, _ = p.getBasePositionAndOrientation(obs_id)
            obs_position = np.array([obs_pos_xyz[0], obs_pos_xyz[1]])
            
            vector_from_obs = current_robot_position - obs_position
            distance_from_obs = np.linalg.norm(vector_from_obs)

            if distance_from_obs < OBSTACLE_RADIUS and distance_from_obs > 0:
                # Force is inversely proportional to distance, pushing away
                repulsive_magnitude = REPULSIVE_GAIN * (1/distance_from_obs - 1/OBSTACLE_RADIUS) * (1/distance_from_obs**2)
                repulsive_force = repulsive_magnitude * (vector_from_obs / distance_from_obs)
                total_repulsive_force += repulsive_force

        # 3. Sum all forces to get the resultant force vector
        resultant_force = attractive_force + total_repulsive_force

        # 4. Convert resultant force to linear and angular velocities for the robot
        # Angle of the resultant force
        desired_heading = np.arctan2(resultant_force[1], resultant_force[0])
        
        # Angular velocity is proportional to the difference in heading
        angular_error = desired_heading - robot_current_yaw
        angular_error = np.arctan2(np.sin(angular_error), np.cos(angular_error)) # Normalize to -pi to pi

        # Linear velocity is proportional to the magnitude of the force (or simply a max value)
        v_linear = np.clip(np.linalg.norm(resultant_force), 0, MAX_LINEAR_VEL)
        omega_angular = np.clip(angular_error * 2.0, -MAX_ANGULAR_VEL, MAX_ANGULAR_VEL) # Simple P control for orientation

        # 5. Apply velocities
        set_differential_drive_velocities(v_linear, omega_angular)

        # Draw resultant force for visualization
        force_end_point = current_robot_position + resultant_force * 0.5 # Scale for visualization
        p.addUserDebugLine(
            lineFromXYZ=[current_robot_position[0], current_robot_position[1], 0.1],
            lineToXYZ=[force_end_point[0], force_end_point[1], 0.1],
            lineColorRGB=[0, 1, 0], lineWidth=3, lifeTime=time_step * 240 * 10)

        # Draw goal
        p.addUserDebugLine(
            lineFromXYZ=[goal_position[0]-0.1, goal_position[1], 0.1],
            lineToXYZ=[goal_position[0]+0.1, goal_position[1], 0.1],
            lineColorRGB=[1, 1, 0], lineWidth=2, lifeTime=0)
        p.addUserDebugLine(
            lineFromXYZ=[goal_position[0], goal_position[1]-0.1, 0.1],
            lineToXYZ=[goal_position[0], goal_position[1]+0.1, 0.1],
            lineColorRGB=[1, 1, 0], lineWidth=2, lifeTime=0)


        # Check if goal reached
        if distance_to_goal < 0.2: # meters
            print("Goal Reached!")
            set_differential_drive_velocities(0, 0)
            break

        p.stepSimulation()
        time.sleep(time_step)

except KeyboardInterrupt:
    print("Simulation interrupted by user.")
finally:
    print("\nPotential Fields Navigation Finished.")
    p.disconnect()
```

### Running the Code & Experimentation

Run the script from your terminal: `python potential_fields.py`.

You will see the racecar attempting to reach the yellow cross (goal). As it approaches the obstacles, you will see it steer around them. The green line represents the resultant force vector guiding the robot.

**Experiment:**
*   **Move obstacles:** Change the `basePosition` of the obstacles to see how the robot reacts.
*   **Change parameters:** Adjust `ATTRACTIVE_GAIN` and `REPULSIVE_GAIN`. What happens if the repulsive gain is too low? What if it's too high?
*   **Local minima:** Try to arrange the obstacles such that the robot gets stuck in a local minimum (e.g., surrounding the goal with obstacles that are too close, creating a "dip" in the potential field before the goal).

## Self-Assessment

1.  What is the primary difference in purpose between global path planning and local reactive navigation?
2.  In the Artificial Potential Field method, how is an obstacle represented conceptually?
3.  What is a "local minimum" in the context of potential fields, and why is it a problem?
4.  Why might a robot combine both a global planner and a local reactive planner?
5.  In the `potential_fields.py` script, how does the repulsive force's magnitude change with respect to the distance from an obstacle?

--- 

**Answer Key:**

1.  **Global path planning** aims to find an optimal path through a *known* environment from start to goal. **Local reactive navigation** focuses on immediate obstacle avoidance and goal attraction based on *current sensor readings* in dynamic or unknown environments.
2.  An obstacle is conceptually represented as a source of **repulsive force** that pushes the robot away.
3.  A local minimum is a configuration where the sum of attractive and repulsive forces on the robot is zero, but the robot has not reached the global goal. This is a problem because the robot can get stuck in such a configuration, unable to move towards the actual goal.
4.  Combining both global and local planning allows the robot to leverage the optimality of a global path while maintaining the ability to react to unforeseen obstacles or dynamic changes in the environment. The global planner provides the overall direction, and the local planner handles immediate safety and navigation.
5.  The repulsive force's magnitude is not just inversely proportional to distance; it is designed to increase very rapidly as the robot gets closer to the obstacle. Specifically, it's proportional to `(1/distance - 1/OBSTACLE_RADIUS) * (1/distance^2)`. This creates a strong pushing effect when very close, but quickly diminishes further away.

## Further Reading

*   [Artificial Potential Fields for Robot Navigation](https://www.youtube.com/watch?v=F2Yt_lUe6L8) - A visual explanation.
*   [Robot Motion Planning: Potential Field Methods](https://cs.stanford.edu/people/latombe/cs326/2005/slides-potential.pdf) - A university lecture slide set (PDF).
*   [Bug Algorithms](https://www.cs.cmu.edu/~motionplanning/lecture/Chap4-Bug-Alg_howie.pdf) - A technical overview of different bug algorithms.
