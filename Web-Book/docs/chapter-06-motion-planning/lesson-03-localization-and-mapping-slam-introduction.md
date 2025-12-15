--- 
title: "Lesson 6.3: Localization and Mapping (SLAM Introduction)"
sidebar_position: 3
description: "Unravel the mysteries of how robots know 'where am I?' and 'what's around me?' by exploring localization, mapping, and the groundbreaking concept of SLAM."
tags: [localization, mapping, slam, odometry, sensors]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Distinguish between the localization problem and the mapping problem in robotics.
*   Understand the fundamental concept of Simultaneous Localization and Mapping (SLAM).
*   Explain how odometry can be used for localization and its inherent limitations.
*   Describe the basic principles of landmark-based localization.
*   Appreciate the challenges of SLAM in real-world environments.

## Prerequisites

*   [Lesson 6.2: Obstacle Avoidance and Reactive Navigation](./lesson-02-obstacle-avoidance-and-reactive-navigation.md)
*   [Lesson 4.3: Mobile Robot Kinematics](../chapter-04-kinematics-and-dynamics/lesson-03-mobile-robot-kinematics.md) (Odometry basics)

## Theory Section

### The Robot's Identity Crisis

Imagine a robot waking up in a new, unknown environment. It has two immediate and intertwined questions:

1.  **Where am I?** (The **Localization Problem**)
    *   Knowing the robot's precise position and orientation (its "pose") within a known map.
    *   This is like knowing your exact spot on a Google Maps-like map.

2.  **What's around me?** (The **Mapping Problem**)
    *   Building a representation of the environment (a "map") while knowing the robot's pose.
    *   This is like drawing a map of a new area while knowing exactly where you are as you draw.

These two problems are often dependent on each other: you need a map to localize, and you need to be localized to build a map. This interdependence leads us to one of the most challenging and exciting areas of robotics: **Simultaneous Localization and Mapping (SLAM)**.

### Odometry: A First Attempt at Localization

As we saw in Lesson 4.3, **odometry** uses wheel encoders to estimate the robot's pose by integrating its movements. It's an excellent start, but it suffers from **cumulative error** due to wheel slip, uneven surfaces, and sensor noise. Over time, the robot's odometry estimate will drift further and further from its true position.

This is why purely odometry-based navigation is often limited to very short distances or controlled environments.

### Localization with a Known Map (Landmark-Based)

If the robot has a pre-existing map, it can correct its odometry drift using **landmarks**. Landmarks are distinctive, recognizable features in the environment (e.g., a specific pole, a unique corner, an RFID tag).

*   **How it works:**
    1.  The robot moves using odometry, which provides an *estimate* of its current pose.
    2.  As the robot encounters and recognizes known landmarks on the map using its sensors (e.g., camera, LiDAR), it measures its distance and/or bearing to these landmarks.
    3.  By comparing these sensor measurements to the expected measurements (given its estimated pose and the known landmark positions on the map), the robot can calculate a correction for its pose estimate.
    4.  This correction reduces the uncertainty in its localization.

This approach is much more robust than odometry alone but requires that a map, with known landmark locations, already exists.

![Localization with Landmarks](https://i.imgur.com/gKkR5aF.png)
*Figure 1: A robot uses its odometry estimate and observations of known landmarks to refine its true position on a map.*

### Simultaneous Localization and Mapping (SLAM)

SLAM is the process by which a robot builds a map of an unknown environment while simultaneously estimating its own location within that map. It's the robot's chicken-and-egg problem: you can't build a good map without knowing your location, and you can't know your location precisely without a good map.

*   **How it works (conceptually):**
    1.  The robot starts with an initial guess of its position and an empty (or partial) map.
    2.  It moves, using odometry to update its pose estimate.
    3.  It senses its environment, detecting potential landmarks or features.
    4.  It adds these new features to its map.
    5.  As it re-observes known features (either landmarks it previously added or existing ones), it uses this information to:
        *   **Correct its pose estimate (localization):** If it observes a feature at a different place than expected, it means its current pose estimate is off.
        *   **Refine the map (mapping):** If its pose estimate becomes more certain, it can place the features it observed on the map with greater accuracy.

    This process constantly refines both the map and the robot's pose in an iterative dance.

*   **Key Challenge: Loop Closure:** One of the biggest challenges in SLAM is **loop closure**. This occurs when a robot revisits a previously visited location. Recognizing that it's back in a familiar place is crucial. If it incorrectly believes it's in a new area, it will create a redundant or inconsistent map. If it correctly identifies loop closure, it can use this information to correct all the accumulated errors (from odometry and mapping) along the entire loop.

### Filters vs. Optimizers in SLAM

Historically, SLAM was tackled using **filters**:
*   **Extended Kalman Filter (EKF) SLAM:** An extension of the Kalman filter, used for non-linear systems. It maintains a single estimate of the robot's pose and the map, updating it with each new observation.
*   **Particle Filter (FastSLAM):** Uses a set of "particles," each representing a possible robot trajectory and map. Observations are used to weigh and resample these particles, converging towards the most likely solution. More robust to non-linearities and multi-modal uncertainties than EKF.

More recently, **optimization-based methods** have become dominant due to increased computational power:
*   **Graph SLAM:** Represents the robot's poses and landmark observations as nodes and edges in a graph. Loop closures create constraints, and the algorithm optimizes the entire graph (all poses and map features) simultaneously to minimize error. This tends to be more accurate, especially for large maps.

## Practical Section

For this exercise, we will implement a very simple conceptual **landmark-based localization** simulation. We'll simulate a robot moving with odometry error and then use observations of known landmarks to correct its position.

### The Code

Create a new file named `simple_localization.py`.

The script defines a set of known `landmarks` in our 2D world. Our robot moves with some added noise (odometry error). When the robot is close enough to "observe" a landmark, we simulate a noisy measurement to that landmark. We then use this measurement and the known landmark position to correct the robot's estimated position.

```python title="simple_localization.py"
import numpy as np
import matplotlib.pyplot as plt
import time

# -- Environment Setup ---
# Known landmarks in the environment (x, y)
landmarks = {
    "LM1": np.array([2.0, 3.0]),
    "LM2": np.array([5.0, 1.0]),
    "LM3": np.array([1.0, 0.5])
}

# -- Robot Parameters ---
robot_true_pose = np.array([0.0, 0.0, 0.0]) # [x, y, yaw] - The actual, hidden pose
robot_estimated_pose = np.array([0.0, 0.0, 0.0]) # Our robot's belief about its pose

ODOMETRY_NOISE_STD = 0.05 # Standard deviation of odometry noise (m/step)
MEASUREMENT_NOISE_STD = 0.2 # Standard deviation of landmark measurement noise (m)
OBSERVATION_RANGE = 2.0 # Max distance to observe a landmark

# -- Simulation Loop ---
dt = 0.1 # Time step
num_steps = 200

# Store history for plotting
true_path_x, true_path_y = [], []
estimated_path_x, estimated_path_y = [], []
corrections_x, corrections_y = [], [] # To visualize where corrections happen

print("Starting Simple Landmark-Based Localization Simulation...")

for i in range(num_steps):
    # 1. Robot movement (True Pose)
    # Move forward with some linear and angular velocity
    true_linear_vel = 0.1
    true_angular_vel = 0.05 * np.sin(i * dt * 0.5) # Oscillate yaw slightly

    robot_true_pose[0] += true_linear_vel * np.cos(robot_true_pose[2]) * dt
    robot_true_pose[1] += true_linear_vel * np.sin(robot_true_pose[2]) * dt
    robot_true_pose[2] += true_angular_vel * dt

    # 2. Odometry Update (Estimated Pose with noise)
    # Assume robot tries to move same as true, but adds noise
    estimated_linear_vel = true_linear_vel + np.random.normal(0, ODOMETRY_NOISE_STD)
    estimated_angular_vel = true_angular_vel + np.random.normal(0, ODOMETRY_NOISE_STD / 5.0)

    robot_estimated_pose[0] += estimated_linear_vel * np.cos(robot_estimated_pose[2]) * dt
    robot_estimated_pose[1] += estimated_linear_vel * np.sin(robot_estimated_pose[2]) * dt
    robot_estimated_pose[2] += estimated_angular_vel * dt
    robot_estimated_pose[2] = np.arctan2(np.sin(robot_estimated_pose[2]), np.cos(robot_estimated_pose[2])) # Normalize yaw

    # 3. Landmark Observation and Correction
    correction_applied = False
    for lm_name, lm_pos in landmarks.items():
        # Check if robot is close enough to observe the landmark (from estimated position)
        distance_to_landmark_est = np.linalg.norm(lm_pos - robot_estimated_pose[:2])

        if distance_to_landmark_est < OBSERVATION_RANGE:
            # Simulate a noisy measurement to the landmark
            true_distance_to_landmark = np.linalg.norm(lm_pos - robot_true_pose[:2])
            measured_distance = true_distance_to_landmark + np.random.normal(0, MEASUREMENT_NOISE_STD)

            # -- Correction Logic (Very Simple: Average the error) ---
            # What is the expected distance based on our current estimate?
            expected_distance = np.linalg.norm(lm_pos - robot_estimated_pose[:2])
            
            # How much error do we have in our distance estimate?
            distance_error = measured_distance - expected_distance

            # Get the unit vector from robot to landmark based on estimate
            direction_vector_est = (lm_pos - robot_estimated_pose[:2]) / expected_distance

            # Apply a fraction of the error as a correction to the estimated position
            # This is a very simplified EKF/localization concept
            correction_factor = 0.5 # How much we trust the measurement vs. odometry
            robot_estimated_pose[:2] += direction_vector_est * distance_error * correction_factor
            
            # Record where correction happened
            if not correction_applied: # Only record one correction per step for visualization clarity
                corrections_x.append(robot_estimated_pose[0])
                corrections_y.append(robot_estimated_pose[1])
                correction_applied = True

    # Store path history
    true_path_x.append(robot_true_pose[0])
    true_path_y.append(robot_true_pose[1])
    estimated_path_x.append(robot_estimated_pose[0])
    estimated_path_y.append(robot_estimated_pose[1])

# -- Plotting ---
plt.figure(figsize=(10, 8))
plt.plot(true_path_x, true_path_y, 'g-', label='True Path')
plt.plot(estimated_path_x, estimated_path_y, 'r--', label='Estimated Path (Odometry + Correction)')
plt.plot(corrections_x, corrections_y, 'bx', markersize=8, label='Correction Points')

for lm_name, lm_pos in landmarks.items():
    plt.plot(lm_pos[0], lm_pos[1], 'ko', markersize=10, label=f'Landmark {lm_name}' if lm_name == "LM1" else "") # Label once
    plt.text(lm_pos[0] + 0.1, lm_pos[1] + 0.1, lm_name)

plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title('Simple Landmark-Based Localization')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()

print("\nSimulation finished. Check the plot for results.")
```

### Running the Code

Run the script from your terminal: `python simple_localization.py`.

A plot will appear. You will see:
*   A **green line** representing the robot's *true* path.
*   A **red dashed line** representing the robot's *estimated* path (which started with odometry drift and was corrected).
*   **Black circles** marking the known landmarks.
*   **Blue crosses** indicating where a significant correction to the estimated path was applied due to a landmark observation.

You should observe that while the estimated path initially drifts due to odometry noise, it gets pulled back towards the true path whenever a landmark is observed, demonstrating the power of external sensing for localization.

## Self-Assessment

1.  What is the primary problem that SLAM aims to solve?
2.  Why is odometry alone insufficient for long-term localization in most real-world scenarios?
3.  How does a landmark help a robot to localize itself?
4.  What is "loop closure" in SLAM, and why is it important?
5.  In the `simple_localization.py` script, what color represents the robot's true path, and what color represents its estimated path?

---

**Answer Key:**

1.  SLAM aims to solve the problem of simultaneously building a map of an unknown environment while also localizing the robot within that map.
2.  Odometry alone is insufficient because it suffers from **cumulative error**; small errors in wheel measurements or movements accumulate over time, causing the robot's estimated position to drift significantly from its true position.
3.  A landmark helps a robot localize itself by providing a known, fixed point of reference. By measuring its distance and/or bearing to a landmark, the robot can compare these measurements to the landmark's known position on the map and correct its estimated pose.
4.  Loop closure in SLAM is when a robot recognizes that it has returned to a previously visited location. It is important because it allows the robot to detect and correct the accumulated errors (from odometry and mapping) that have occurred along the entire loop, significantly improving the accuracy of both the map and the robot's estimated trajectory.
5.  The **green line** represents the robot's true path, and the **red dashed line** represents its estimated path.

## Further Reading

*   [SLAM (Simultaneous Localization And Mapping) Explained](https://www.youtube.com/watch?v=Fj-y51d02S8) - A great animated overview of SLAM.
*   [How a Robot Builds a Map and Knows Where It Is](https://www.youtube.com/watch?v=saV72F0G-oQ) - Another excellent visual introduction.
*   *Probabilistic Robotics, Chapter 7: Mobile Robot Localization* - An in-depth chapter from a classic textbook.
