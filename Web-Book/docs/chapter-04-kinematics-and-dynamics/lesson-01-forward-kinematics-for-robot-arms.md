--- 
title: "Lesson 4.1: Forward Kinematics for Robot Arms"
sidebar_position: 1
description: "An introduction to the mathematics of robot motion, exploring coordinate frames, transformations, and how to calculate a robot's end-effector position."
tags: [kinematics, forward-kinematics, transformations, robotics-math]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Define forward kinematics and explain its importance.
*   Understand coordinate frames and how they are attached to a robot's links.
*   Describe how to combine translation and rotation using transformation matrices.
*   Calculate the end-effector position of a simple 2D robot arm using trigonometry.
*   Use PyBullet to verify the forward kinematics of a multi-jointed robot arm.

## Prerequisites

*   [Lesson 3.3: Programming Basic Movements](../chapter-03-actuators-and-control/lesson-03-programming-basic-movements.md)
*   Basic knowledge of trigonometry (sine, cosine).

## Theory Section

### The Question of Kinematics

**Kinematics** is the study of motion without considering the forces that cause it. In robotics, it's the math that connects the robot's joint parameters (like motor angles) to the position and orientation of its parts.

There are two fundamental problems in kinematics:

1.  **Forward Kinematics (FK):** If I know the angles of all my robot's joints, where is the robot's hand (or "end-effector") in space? This is the "easy" problem, and it's what we'll cover in this lesson.
2.  **Inverse Kinematics (IK):** If I want to place my robot's end-effector at a specific target position and orientation, what angles do I need to set my joints to? This is the "hard" problem, which we will cover in the next lesson.

Forward kinematics is essential for any robot arm. If the robot doesn't know where its own hand is, it can't perform any useful tasks.

### Coordinate Frames

To describe the position of different parts of a robot, we attach **coordinate frames** to them. A coordinate frame is just an origin point and a set of X, Y, and Z axes.

*   A **base frame** (`{0}`) is fixed to the non-moving base of the robot.
*   A **link frame** is attached to each moving link of the robot.
*   An **end-effector frame** (`{E}`) is attached to the robot's tool or gripper.

The goal of forward kinematics is to find the position and orientation of the end-effector frame `{E}` relative to the base frame `{0}`.

![Robot Arm with Coordinate Frames](https://i.imgur.com/g0i0tGg.png)
*Figure 1: A 2-link robot arm with a coordinate frame attached to each link.*

### Forward Kinematics of a 2D Arm (The Easy Way)

Let's start with the simple 2-link arm in Figure 1. It has two links of lengths `L1` and `L2`, and two joints with angles `θ1` (theta-1) and `θ2` (theta-2). We want to find the (x, y) coordinates of the end-effector.

We can solve this using basic trigonometry.

1.  **Find the position of the first joint (P1):**
    *   The first joint is at the end of the first link.
    *   `x1 = L1 * cos(θ1)`
    *   `y1 = L1 * sin(θ1)`

2.  **Find the position of the end-effector (P_E) relative to the first joint:**
    *   The second link's angle is relative to the first link. So, its angle with respect to the base frame's X-axis is `θ1 + θ2`.
    *   `x_relative = L2 * cos(θ1 + θ2)`
    *   `y_relative = L2 * sin(θ1 + θ2)`

3.  **Add them together to get the final position:**
    *   `x_E = x1 + x_relative = L1 * cos(θ1) + L2 * cos(θ1 + θ2)`
    *   `y_E = y1 + y_relative = L1 * sin(θ1) + L2 * sin(θ1 + θ2)`

These are the **forward kinematics equations** for our simple 2D arm. Given any `θ1` and `θ2`, we can compute the `(x_E, y_E)` position of the end-effector.

### The Problem with Scaling Up: Transformations

Trigonometry works for a 2-link arm, but it quickly becomes a nightmare for a 6- or 7-jointed 3D robot. We need a more systematic approach.

The solution is to use **transformation matrices**. A transformation matrix is a 4x4 matrix that can describe both the **rotation** and **translation** of one coordinate frame relative to another.

A transformation matrix `T` from frame `A` to frame `B` looks like this:

```
    | R R R T_x |
T = | R R R T_y |
    | R R R T_z |
    | 0 0 0 1   |
```

- R = Rotation matrix part
- T = Translation vector part

The power of this approach is that we can chain transformations together using matrix multiplication. To get the transformation from the base `{0}` to the end-effector `{E}`, we can find the transformation for each joint and multiply them:

`T_0_E = T_0_1 * T_1_2 * T_2_3 * ... * T_N_E`

This is the core of modern robotics kinematics. For a standard robot arm, there is a systematic way to derive these transformation matrices called the **Denavit-Hartenberg (DH) convention**. While the details of DH parameters are beyond the scope of this lesson, the key takeaway is that it provides a recipe for describing the geometry of any robot arm and deriving its forward kinematics automatically.

PyBullet and other robotics software handle all of this matrix math for you. When you ask for the state of a link, it performs these calculations internally to give you the final position and orientation.

## Practical Section

In this exercise, we will use PyBullet to perform forward kinematics. We will load a 6-axis robot arm, set its joint angles manually, and then use a PyBullet function to tell us the resulting position of its end-effector. This lets us verify the principles of FK without doing the complex 3D math ourselves.

### The Code

Create a new file named `forward_kinematics.py`.

The script loads a KUKA robot arm. We then define a set of target angles for each of its 6 joints. We loop through, setting each joint to its target angle. Finally, we call `p.getLinkState` on the end-effector link (link index 6) to get its Cartesian position and orientation.

``` title="forward_kinematics.py"
import pybullet as p
import time
import pybullet_data
import math

# --- Setup ---
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -10)

# Load a plane and a robot arm (KUKA LBR iiwa)
robot_id = p.loadURDF("kuka_lbr_iiwa/model.urdf", basePosition=[0,0,0], useFixedBase=True)

# The end-effector is the 6th link (0-indexed)
end_effector_link_index = 6

# --- Forward Kinematics Demonstration ---

# 1. Define a set of target joint angles (in radians)
# These are the "known" joint angles for our FK problem
target_joint_angles = [
    math.radians(30),   # Joint 1
    math.radians(45),   # Joint 2
    math.radians(0),    # Joint 3
    math.radians(-60),  # Joint 4
    math.radians(0),    # Joint 5
    math.radians(90)    # Joint 6
]
print(f"Target Joint Angles (radians): {[f'{a:.2f}' for a in target_joint_angles]}")

# 2. Set the joints to the target angles
# In a real robot, this would involve commanding the motors.
# In PyBullet, we can use a position controller.
num_joints = p.getNumJoints(robot_id)
for i in range(num_joints):
    p.setJointMotorControl2(
        bodyIndex=robot_id,
        jointIndex=i,
        controlMode=p.POSITION_CONTROL,
        targetPosition=target_joint_angles[i],
        force=500 # Apply enough force to hold the position
    )

# Let the simulation run for a bit for the arm to settle
for _ in range(240 * 2):
    p.stepSimulation()
    time.sleep(1./240.)


# 3. Get the state of the end-effector
# This is the "answer" to our forward kinematics problem
# PyBullet does the complex math for us!
end_effector_state = p.getLinkState(robot_id, end_effector_link_index)
end_effector_pos = end_effector_state[0] # World position (x, y, z)
end_effector_ori = end_effector_state[1] # World orientation (quaternion)

print("\n--- Forward Kinematics Result ---")
print(f"Given the joint angles, the end-effector is at:")
print(f"Position (x, y, z): ({end_effector_pos[0]:.3f}, {end_effector_pos[1]:.3f}, {end_effector_pos[2]:.3f})")

# Quaternions are hard to read, let's convert to Euler angles
end_effector_euler = p.getEulerFromQuaternion(end_effector_ori)
print(f"Orientation (roll, pitch, yaw): ({math.degrees(end_effector_euler[0]):.1f}°, {math.degrees(end_effector_euler[1]):.1f}°, {math.degrees(end_effector_euler[2]):.1f}°)")

# Keep the simulation running to observe
print("\nSimulation will run for 10 more seconds.")
for _ in range(240 * 10):
    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()
```

### Running the Code

Run the script from your terminal: `python forward_kinematics.py`.

The KUKA arm will move to the specified joint configuration. Your terminal will then print the calculated Cartesian coordinates (X, Y, Z position) and orientation of the end-effector. This is the forward kinematics solution! You have answered the question: "Given these joint angles, where is the hand?"

## Self-Assessment

1.  What is the core question that forward kinematics answers?
2.  In the 2D arm example, why do we use `cos(θ1 + θ2)` for the second link?
3.  What two types of information can be stored in a 4x4 transformation matrix?
4.  If you have a 3-link arm, and you know the transformations `T_0_1`, `T_1_2`, and `T_2_3`, how do you find the total transformation from the base to the end-effector, `T_0_3`?
5.  In the PyBullet code, what function is used to get the final answer to the FK problem?

---

**Answer Key:**

1.  Forward kinematics answers the question: "If I know the state of all my robot's joints, where is my end-effector (or any other part of the robot) in space?"
2.  Because the second joint's angle (`θ2`) is measured relative to the first link. To get its angle in the world frame, we must add it to the first link's angle (`θ1`).
3.  A 4x4 transformation matrix can store both **rotation** (in the upper-left 3x3 sub-matrix) and **translation** (in the upper-right 3x1 vector).
4.  You find the total transformation by multiplying the individual transformations in order: `T_0_3 = T_0_1 * T_1_2 * T_2_3`.
5.  The `p.getLinkState()` function.

## Further Reading

*   [Introduction to Robot Kinematics](https://www.youtube.com/watch?v=g_S5W6-Vv_c) - A visual introduction from the "Robotics & Control" YouTube channel.
*   [Modern Robotics, Chapter 3: Rigid-Body Motions](http://hades.mech.northwestern.edu/index.php/Modern_Robotics) - A university-level textbook chapter on the topic (mathematically intensive).
*   [3Blue1Brown: Linear transformations and matrices](https://www.youtube.com/watch?v=kYB8IZa5AuE) - A fantastic and intuitive explanation of the matrix math behind transformations.
