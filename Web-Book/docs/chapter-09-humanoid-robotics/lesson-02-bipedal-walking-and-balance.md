--- 
title: "Lesson 9.2: Bipedal Walking and Balance"
sidebar_position: 2
description: "Uncover the secrets of bipedal locomotion, from gait cycles and dynamic balance to walking pattern generation and push recovery, using the inverted pendulum model."
tags: [humanoid-robotics, bipedal-walking, balance, dynamic-stability, gait]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Describe the phases of a bipedal gait cycle (stance, swing, double support).
*   Differentiate between static and dynamic balance.
*   Understand the Inverted Pendulum Model as a simplified model for walking.
*   Explain the role of a Walking Pattern Generator in creating smooth locomotion.
*   Implement a simple walking controller for a simulated humanoid robot.

## Prerequisites

*   [Lesson 9.1: Humanoid Robot Design and Kinematics](./lesson-01-humanoid-robot-design-and-kinematics.md)

## Theory Section

### The Art of Controlled Falling

Walking is one of the most challenging control problems in robotics. It's not a static process; it's a dynamic one. Bipedal walking is often described as a continuous process of "controlled falling," where the robot intentionally falls forward and then catches itself with the next step.

### The Bipedal Gait Cycle

A **gait cycle** is the sequence of movements that occurs from the moment one foot touches the ground to the moment the *same* foot touches the ground again. It can be broken down into several phases:

1.  **Stance Phase:** The period when a foot is in contact with the ground.
2.  **Swing Phase:** The period when a foot is in the air, moving forward for the next step.
3.  **Double Support Phase:** The brief period when *both* feet are on the ground (typically at the beginning and end of a stance phase). This phase provides the most stability.
4.  **Single Support Phase:** The period when only one foot is on the ground, and the other is swinging. This is the most unstable phase of walking.

    ![Gait Cycle](https://i.imgur.com/gKkR5aF.png)
    *Figure 1: The phases of a human gait cycle. Robotic walking mimics this sequence.*

### Static vs. Dynamic Balance

*   **Static Balance:** A state where the robot's center of gravity (CoG) is vertically aligned over its support polygon. This is how a robot stands still. A statically balanced walk would mean the robot moves so slowly that its CoG is *always* over the support foot, which is very slow and inefficient.
*   **Dynamic Balance:** A state where the robot is in motion and uses its momentum and planned movements to maintain balance, even if its CoG is temporarily outside its support polygon. This is how humans and advanced robots walk. The key is to ensure the **Zero Moment Point (ZMP)** stays within the support polygon.

### The Inverted Pendulum Model

To simplify the incredibly complex problem of controlling a high-DoF humanoid, engineers often use a simplified model. The most common is the **Linear Inverted Pendulum Model (LIPM)**.

*   **How it works:** The model assumes the robot's entire mass is concentrated at its center of mass (CoM), and its legs are massless stilts. The dynamics of the robot's CoM can then be modeled as an inverted pendulum.
*   **Why it's useful:** The LIPM provides a direct relationship between the robot's CoM and the ZMP. This allows a controller to plan a trajectory for the CoM that will produce a desired trajectory for the ZMP, ensuring that the ZMP stays within the support polygon (the feet) throughout the gait cycle.

    `ZMP_x = CoM_x - (CoM_z / g) * d^2(CoM_x)/dt^2`

This equation shows that the ZMP position depends on the CoM position and its acceleration. To keep the ZMP stable, we must control the acceleration of the CoM.

### Walking Pattern Generation

A **Walking Pattern Generator** is a high-level controller that uses a simplified model like the LIPM to generate reference trajectories for the robot's center of mass and feet.

1.  **Input:** Desired walking parameters (e.g., step length, step height, walking speed, direction).
2.  **Process:** The generator plans a ZMP trajectory that moves smoothly from one foot to the next. Using the LIPM equations, it then calculates the corresponding CoM trajectory that will produce this ZMP trajectory. It also generates trajectories for the swing foot to lift off, move forward, and land.
3.  **Output:** A set of reference trajectories for the CoM and each foot.
4.  **Execution:** These reference trajectories are then fed into a whole-body controller, which uses Inverse Kinematics and other control methods to calculate the required joint angles for the legs, arms, and torso to achieve the desired motion.

### Push Recovery: Reacting to the Unexpected

What happens if someone pushes the robot while it's walking? A robust walking controller must be able to handle external disturbances. This is known as **push recovery**.

*   **How it works:**
    1.  **Sensing:** The robot's IMU detects a sudden, unexpected acceleration.
    2.  **Estimation:** The controller estimates the magnitude and direction of the external force.
    3.  **Correction:** The controller rapidly modifies its plan to counteract the push. This can involve:
        *   **Ankle Strategy:** Making small adjustments by applying torque at the ankles.
        *   **Hip Strategy:** Making larger adjustments by bending at the hips to shift the CoM.
        *   **Stepping Strategy:** Taking an extra step to widen the support polygon and regain balance.

## Practical Section

Implementing a full dynamic walking controller is extremely complex and beyond the scope of a single lesson. However, we can create a simplified, "kinematic" or "scripted" walking animation in PyBullet. This will demonstrate the core concepts of gait sequencing and coordinating leg movements, even without a dynamic balance controller.

We will load a simple humanoid model and use a state machine to move its leg joints through a predefined sinusoidal trajectory, creating the illusion of walking.

### The Code

Create a new Python file named `kinematic_walking.py`.

The script loads PyBullet's built-in `humanoid.urdf` model. We then use a `time` variable to drive a set of sine and cosine functions. These functions generate cyclical target angles for the hip and knee joints of each leg, creating an alternating walking motion.

```python title="kinematic_walking.py"
import pybullet as p
import time
import pybullet_data
import math

# --- Setup ---
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.setRealTimeSimulation(0)

planeId = p.loadURDF("plane.urdf")
humanoid = p.loadURDF("humanoid/humanoid.urdf", basePosition=[0, 0, 1.2])

# --- Joint and Gait Parameters ---
# Get joint indices for legs from the URDF
# In humanoid.urdf:
# Right leg: hip (1), knee (2), ankle (3)
# Left leg: hip (4), knee (5), ankle (6)
right_hip_joint = 1
right_knee_joint = 2
left_hip_joint = 4
left_knee_joint = 5

# Gait parameters
amplitude = 0.5  # radians (approx 30 degrees)
frequency = 1.0  # Hz (1 step per second)
phase_offset = math.pi # Left leg is 180 degrees out of phase with right leg

# --- Main Simulation Loop ---
print("Starting Kinematic Walking Simulation...")
print("This is a scripted animation, not a dynamic balance controller.")

start_time = time.time()
try:
    while True:
        # Calculate current time in the gait cycle
        t = time.time() - start_time
        
        # 1. Calculate target angles for each joint using sine waves
        
        # Right Leg
        target_hip_right = amplitude * math.cos(2 * math.pi * frequency * t)
        # Knee bends when hip moves forward
        target_knee_right = amplitude * (math.cos(2 * math.pi * frequency * t) + 1) / 2
        
        # Left Leg (out of phase)
        target_hip_left = amplitude * math.cos(2 * math.pi * frequency * t + phase_offset)
        target_knee_left = amplitude * (math.cos(2 * math.pi * frequency * t + phase_offset) + 1) / 2
        
        # 2. Set joint positions using position control
        p.setJointMotorControl2(
            bodyIndex=humanoid,
            jointIndex=right_hip_joint,
            controlMode=p.POSITION_CONTROL,
            targetPosition=target_hip_right,
            force=500
        )
        p.setJointMotorControl2(
            bodyIndex=humanoid,
            jointIndex=right_knee_joint,
            controlMode=p.POSITION_CONTROL,
            targetPosition=target_knee_right,
            force=500
        )
        p.setJointMotorControl2(
            bodyIndex=humanoid,
            jointIndex=left_hip_joint,
            controlMode=p.POSITION_CONTROL,
            targetPosition=target_hip_left,
            force=500
        )
        p.setJointMotorControl2(
            bodyIndex=humanoid,
            jointIndex=left_knee_joint,
            controlMode=p.POSITION_CONTROL,
            targetPosition=target_knee_left,
            force=500
        )
        
        # Make the robot "float" forward to simulate forward motion
        # In a real walking controller, this forward motion would be a result of the dynamics
        current_pos, _ = p.getBasePositionAndOrientation(humanoid)
        new_pos = [current_pos[0] + 0.005, current_pos[1], current_pos[2]] # Move slowly in X
        # p.resetBasePositionAndOrientation(humanoid, new_pos, p.getQuaternionFromEuler([0,0,0]))
        
        p.stepSimulation()
        time.sleep(1./240.)
        
except KeyboardInterrupt:
    print("Simulation interrupted.")
finally:
    print("\nKinematic Walking Simulation Finished.")
    p.disconnect()
```

### Running the Code

Run the script from your terminal: `python kinematic_walking.py`.

You will see the humanoid model in PyBullet begin to move its legs in a walking-like motion. The right and left legs will move in opposite phases, mimicking a natural gait. Note that the robot is likely to fall over, as we have not implemented any dynamic balance control – this is purely a *kinematic* animation. It demonstrates how to generate the necessary joint trajectories, which is the first step in creating a full walking controller.

## Self-Assessment

1.  What is the difference between the "swing phase" and the "stance phase" in a gait cycle?
2.  Why is dynamic balance necessary for efficient walking, as opposed to static balance?
3.  What is the main purpose of the Linear Inverted Pendulum Model (LIPM) in walking pattern generation?
4.  What are the three main "strategies" a robot can use for push recovery?
5.  In the `kinematic_walking.py` script, what mathematical function is used to create the smooth, cyclical motion of the legs?

---

**Answer Key:**

1.  The **swing phase** is when a foot is in the air, moving forward for the next step. The **stance phase** is when a foot is in contact with the ground, supporting the body's weight.
2.  Dynamic balance allows the robot to use its momentum to "fall" into the next step, which is much faster and more energy-efficient than the slow, shuffling motion required to keep the center of gravity over the support foot at all times (static balance).
3.  The LIPM simplifies the complex dynamics of the humanoid robot, providing a direct mathematical relationship between the robot's Center of Mass (CoM) trajectory and its Zero Moment Point (ZMP). This allows controllers to plan a CoM motion that guarantees the ZMP will remain in a stable location.
4.  The three main strategies are the **Ankle Strategy** (small adjustments), the **Hip Strategy** (larger adjustments), and the **Stepping Strategy** (taking a step to regain balance).
5.  The script uses trigonometric **sine and cosine functions** to generate smooth, periodic target angles for the hip and knee joints.

## Further Reading

*   [How Humanoid Robots Walk](https://www.youtube.com/watch?v=kYJru4a3t5o) - A good high-level overview.
*   [The Science of the Inverted Pendulum Model](https://www.youtube.com/watch?v=g_S5W6-Vv_c) - A deeper dive into the physics of walking.
*   [Push Recovery in Humanoid Robots](https://www.youtube.com/watch?v=tF4DML7FIWk) - Watch Boston Dynamics' Atlas robot demonstrate impressive push recovery.
*   *Humanoid Robotics: A Reference* by Ambarish Goswami and P. Vadakkepat - A comprehensive textbook on the subject.
