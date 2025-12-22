--- 
title: "Lesson 4.3: Mobile Robot Kinematics"
sidebar_position: 3
description: "Explore how wheeled mobile robots move, including differential drive, car-like, and omnidirectional platforms, and learn about odometry and its limitations."
tags: [kinematics, mobile-robotics, odometry, differential-drive, omnidirectional]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Describe the kinematic models of common wheeled mobile robot platforms (differential drive, car-like, omnidirectional).
*   Calculate the linear and angular velocity of a differential drive robot given its wheel speeds.
*   Understand the concept of odometry and how it's used to estimate a robot's position.
*   Identify the limitations and sources of error in odometry.
*   Implement basic waypoint navigation for a differential drive robot in simulation.

## Prerequisites

*   [Lesson 4.1: Forward Kinematics for Robot Arms](./lesson-01-forward-kinematics-for-robot-arms.md) (Understanding of coordinate frames and transformations)
*   [Lesson 3.3: Programming Basic Movements](../chapter-03-actuators-and-control/lesson-03-programming-basic-movements.md) (Basic robot motion control)

## Theory Section

### Moving Across the Ground

Unlike robot arms, which move their end-effectors in space, **mobile robots** move their entire base across a surface. Their kinematics focuses on how the motion of their wheels translates into the robot's overall motion (linear and angular velocity) and how to estimate its position over time.

We'll look at three common types of wheeled mobile robots:

#### 1. Differential Drive Robots

*   **Description:** Two independently driven wheels on a common axis, with passive caster wheels for stability.
*   **How it Moves:**
    *   **Forward/Backward:** Both wheels turn at the same speed in the same direction.
    *   **Turning:** Wheels turn at different speeds or in opposite directions.
*   **Kinematics:** Simple and widely used (e.g., Roomba, many educational robots).
    *   Let `v_L` and `v_R` be the linear velocities of the left and right wheels, respectively.
    *   Let `r` be the wheel radius.
    *   Let `L` be the distance between the two wheels (wheelbase).
    *   Robot's **linear velocity (v)**: `v = (v_L + v_R) / 2`
    *   Robot's **angular velocity (ω)**: `ω = (v_R - v_L) / L`

    These equations allow us to determine the robot's movement from its wheel speeds. Conversely, we can use them to find the required wheel speeds to achieve a desired `v` and `ω`.

#### 2. Car-Like Robots (Ackermann Steering)

*   **Description:** Similar to an automobile, with two steerable front wheels and two fixed rear wheels (or vice-versa).
*   **How it Moves:** Steering angle determines turning radius, and wheel speed determines linear velocity.
*   **Kinematics:** More complex than differential drive, as both steering angle and wheel rotation must be controlled. Typically non-holonomic (cannot move sideways).
*   **Applications:** Autonomous cars, forklifts, larger outdoor mobile platforms.

#### 3. Omnidirectional Robots

*   **Description:** Use special wheels (e.g., Mecanum wheels or omni-wheels) that allow movement in any direction (forward, backward, sideways, and rotation) without changing the orientation of the wheels.
*   **How it Moves:** By coordinating the speed and direction of multiple omni-wheels, the robot can move in any direction.
*   **Kinematics:** Most complex, requiring precise control of each wheel. Holonomic (can move in any direction instantly).
*   **Applications:** Manufacturing floors, tight spaces where high maneuverability is needed.

### Odometry: Estimating Your Position

**Odometry** is the process of estimating a robot's current position and orientation (its "pose") by integrating information from its wheel encoders. It's the most common and often the only form of localization available for many mobile robots.

*   **How it works:**
    1.  Measure how far each wheel has rotated using encoders.
    2.  Calculate the linear distance traveled by each wheel (`distance = wheel_radius * angle_rotated`).
    3.  Use the kinematic model (e.g., differential drive equations) to infer the robot's change in `(x, y)` position and `θ` orientation.
    4.  Accumulate these small changes over time to get the robot's estimated current pose.

    `New_Pose = Old_Pose + Change_in_Pose`

### Limitations and Errors of Odometry

While simple, odometry is prone to accumulating errors over time because it's an **integration process**. Even tiny measurement errors or environmental factors can lead to significant drift.

**Common sources of error:**

*   **Wheel Slip:** If wheels slip on the ground (e.g., due to acceleration, slippery surfaces, uneven terrain), the encoder will report movement that didn't actually translate to robot motion.
*   **Uneven Wheel Diameters:** Small manufacturing differences in wheel size can lead to cumulative errors.
*   **Encoder Resolution:** Limited precision in angle measurement.
*   **Alignment Errors:** Wheels not perfectly parallel or perpendicular to the robot's chassis.
*   **Uneven Surfaces:** Bumps or divots can cause the robot to bounce or wheels to temporarily lose contact.

Because of these limitations, odometry is almost always combined with other sensors (like GPS, IMUs, LiDAR, or cameras) using **sensor fusion** techniques (which we touched on in Lesson 2.3) to provide more robust and accurate localization.

## Practical Section

In this exercise, we will program a differential drive robot (our racecar from Lesson 3.3) to navigate to a series of waypoints using a simple odometry-based approach. We will command target linear and angular velocities to reach each waypoint.

### The Code

Create a new file named `waypoint_navigation.py`.

This script enhances our `set_wheel_velocities` function to calculate individual wheel speeds from desired linear and angular velocities. We then define a list of `waypoints`. The robot iteratively moves towards each waypoint by calculating the required linear (`v`) and angular (`omega`) velocity, and then translates these into commands for the left and right wheels.

```python title="waypoint_navigation.py"
import pybullet as p
import time
import pybullet_data
import math
import numpy as np

# --- Robot Parameters (Adjust these to match your robot model if needed) ---
WHEEL_RADIUS = 0.1 # Example: meters
WHEEL_BASE = 0.5   # Distance between wheels, meters

# --- Setup ---
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -10)
p.setRealTimeSimulation(0) # We will manually step the simulation

planeId = p.loadURDF("plane.urdf")
car = p.loadURDF("racecar/racecar.urdf", basePosition=[0, 0, 0.2])

# The racecar model has 4 wheel joints (indices 2, 3, 5, 7)
left_rear_wheel_index = 5
right_rear_wheel_index = 7

# --- Odometry (Simulated) ---
# We'll keep track of the robot's estimated pose
# [x, y, yaw]
robot_pose = np.array([0.0, 0.0, 0.0]) # Start at origin, facing X+

# Helper to update pose based on kinematics
def update_pose(current_pose, v_linear, omega_angular, dt):
    x, y, yaw = current_pose
    if abs(omega_angular) < 1e-6: # Moving straight
        x += v_linear * np.cos(yaw) * dt
        y += v_linear * np.sin(yaw) * dt
    else: # Turning
        # Radius of curvature
        R = v_linear / omega_angular
        # Instantaneous Center of Curvature (ICC)
        icc_x = x - R * np.sin(yaw)
        icc_y = y + R * np.cos(yaw)

        # Update pose
        x = icc_x + R * np.sin(yaw + omega_angular * dt)
        y = icc_y - R * np.cos(yaw + omega_angular * dt)
        yaw += omega_angular * dt
    return np.array([x, y, yaw])


# --- Control Functions ---
def set_differential_drive_velocities(v_linear, omega_angular):
    """
    Calculates and sets the individual wheel velocities for a differential drive robot
    based on desired linear and angular velocities.
    """
    v_left = (v_linear - (omega_angular * WHEEL_BASE / 2))
    v_right = (v_linear + (omega_angular * WHEEL_BASE / 2))

    # Convert linear wheel velocity to angular wheel velocity (rad/s)
    target_left_ang_vel = v_left / WHEEL_RADIUS
    target_right_ang_vel = v_right / WHEEL_RADIUS

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

# --- Waypoints and Navigation Logic ---
waypoints = [
    np.array([2.0, 0.0]), # Go forward
    np.array([2.0, 2.0]), # Turn left
    np.array([0.0, 2.0]), # Turn left again
    np.array([0.0, 0.0])  # Return to start
]
current_waypoint_idx = 0

K_P_linear = 1.0 # Proportional gain for linear velocity
K_P_angular = 2.0 # Proportional gain for angular velocity
target_distance_threshold = 0.1 # meters
time_step = 1.0/240.0 # PyBullet's default time step

# Keep track of simulation time
sim_start_time = time.time()
last_update_time = sim_start_time

print("Starting waypoint navigation...")

try:
    while current_waypoint_idx < len(waypoints):
        target_waypoint = waypoints[current_waypoint_idx]
        current_position = robot_pose[:2] # X, Y components

        # Calculate vector from robot to target
        vector_to_target = target_waypoint - current_position
        distance_to_target = np.linalg.norm(vector_to_target)

        # Calculate desired heading to target
        target_yaw = np.arctan2(vector_to_target[1], vector_to_target[0])

        # Calculate angular error (difference between robot's current yaw and target yaw)
        yaw_error = target_yaw - robot_pose[2]
        yaw_error = np.arctan2(np.sin(yaw_error), np.cos(yaw_error)) # Normalize to -pi to pi

        # Simple controller: if not aligned, just turn. If aligned, move forward.
        v_linear = 0.0
        omega_angular = 0.0

        if distance_to_target > target_distance_threshold:
            if abs(yaw_error) > math.radians(5): # If error is more than 5 degrees
                omega_angular = K_P_angular * yaw_error
                # Limit angular velocity
                omega_angular = np.clip(omega_angular, -math.pi/2, math.pi/2)
            else: # Aligned, move forward
                v_linear = K_P_linear * distance_to_target
                # Limit linear velocity
                v_linear = np.clip(v_linear, 0, 1.0)
                omega_angular = K_P_angular * yaw_error # Still correct small yaw errors while moving

            set_differential_drive_velocities(v_linear, omega_angular)
        else:
            print(f"Reached waypoint {current_waypoint_idx+1}/{len(waypoints)}: {target_waypoint}")
            set_differential_drive_velocities(0, 0) # Stop
            current_waypoint_idx += 1
            if current_waypoint_idx < len(waypoints):
                print(f"Moving to next waypoint: {waypoints[current_waypoint_idx]}")
            time.sleep(1.0) # Pause at waypoint

        # Step simulation and update odometry
        p.stepSimulation()
        robot_pose = update_pose(robot_pose, v_linear, omega_angular, time_step)
        
        # Draw current pose for visualization (X, Y, Z) and Yaw (represented by arrow)
        p.addUserDebugLine(
            lineFromXYZ=[robot_pose[0], robot_pose[1], 0.01],
            lineToXYZ=[robot_pose[0] + 0.5 * np.cos(robot_pose[2]),
                       robot_pose[1] + 0.5 * np.sin(robot_pose[2]), 0.01],
            lineColorRGB=[1, 0, 0], lineWidth=2, lifeTime=time_step * 240 * 10)
        
        time.sleep(time_step)

finally:
    print("\nWaypoint navigation finished.")
    set_differential_drive_velocities(0, 0) # Ensure robot is stopped
    p.disconnect()
```

### Running the Code

Run the script from your terminal: `python waypoint_navigation.py`.

You will see the racecar in the simulation window attempting to navigate to each waypoint in the predefined sequence. A red line will indicate the robot's current estimated heading. In the terminal, you'll see messages as the robot reaches each waypoint.

This exercise provides a basic demonstration of how odometry and simple control can be used for mobile robot navigation.

## Self-Assessment

1.  How does a differential drive robot achieve pure rotation (spinning in place)?
2.  What is the primary purpose of odometry in mobile robotics?
3.  Name two significant sources of error that can cause odometry to drift.
4.  If a differential drive robot's left wheel spins at `10 rad/s` and its right wheel spins at `5 rad/s` (both forward), will the robot turn left or right?
5.  In the `update_pose` function, what is the role of `dt`?

---

**Answer Key:**

1.  A differential drive robot achieves pure rotation by spinning its left and right wheels in opposite directions at the same speed.
2.  The primary purpose of odometry is to estimate the robot's current position and orientation (pose) by integrating data from its wheel encoders.
3.  Common sources of error include wheel slip, uneven wheel diameters, encoder resolution limitations, and misalignment of wheels.
4.  The robot will turn **left** because the right wheel is spinning slower, causing the robot to pivot around the slower wheel's side.
5.  `dt` represents the time step or the duration over which the movement occurs. It's crucial for converting velocities (meters/second, radians/second) into distances and angles (meters, radians) traveled over that small time interval.

## Further Reading

*   [Kinematic Model of a Differential Drive Robot](https://www.youtube.com/watch?v=F0S12T4R5Kk) - A clear video explanation of the math.
*   [Introduction to Mobile Robot Odometry](https://www.robotc.net/wiki/Tutorials/Differential_Drive_Robot_Kinematics) - A comprehensive article on odometry.
*   [Mecanum Wheel Kinematics](https://www.youtube.com/watch?v=Lbbp5K2rXU4) - For those curious about omnidirectional robots.
