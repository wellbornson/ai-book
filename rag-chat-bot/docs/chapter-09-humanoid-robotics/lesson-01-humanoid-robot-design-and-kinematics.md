--- 
title: "Lesson 9.1: Humanoid Robot Design and Kinematics"
sidebar_position: 1
description: "Step into the world of humanoid robotics by exploring their design, anatomy, kinematic chains, and the crucial concept of the Zero Moment Point (ZMP) for balance."
tags: [humanoid-robotics, kinematics, degrees-of-freedom, zmp]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Identify the key components of a humanoid robot's anatomy (legs, torso, arms, head).
*   Define Degrees of Freedom (DoF) and explain why humanoids have a high DoF.
*   Understand the concept of a kinematic chain as it applies to humanoid robots.
*   Explain the Zero Moment Point (ZMP) and its critical role in maintaining balance.
*   Model a simple humanoid robot in PyBullet and calculate its ZMP.

## Prerequisites

*   [Lesson 4.1: Forward Kinematics for Robot Arms](../chapter-04-kinematics-and-dynamics/lesson-01-forward-kinematics-for-robot-arms.md)
*   [Lesson 8.1: Gripper Design and Force Control](../chapter-08-manipulation/lesson-01-gripper-design-and-force-control.md)

## Theory Section

### The Ultimate Robotic Challenge: Building a Human

**Humanoid robotics** is a branch of robotics focused on creating robots with a body structure and movement capabilities resembling those of a human. This is an immense challenge because the human body is a masterpiece of engineering, capable of incredible feats of balance, dexterity, and dynamic motion.

The goal is not just to mimic the human form, but to enable robots to operate effectively in human-centric environments – using our tools, navigating our homes, and interacting with us intuitively.

### Humanoid Anatomy and Degrees of Freedom (DoF)

A typical humanoid robot is composed of several key parts, each contributing to its overall mobility.

*   **Legs:** Provide locomotion (walking, running, climbing stairs). A human leg has 7 DoF (3 at the hip, 1 at the knee, 3 at the ankle). Robot legs often have 5 or 6 DoF for simplicity.
*   **Torso:** Connects the legs to the upper body. Can provide additional DoF for bending and twisting, crucial for balance and reach.
*   **Arms:** Used for manipulation, similar to the industrial arms we've studied. Typically have 6 or 7 DoF.
*   **Head:** Houses sensors (cameras, microphones) and often has 2 or 3 DoF (pan, tilt, roll) to direct the robot's "gaze."

The **Degrees of Freedom (DoF)** of a robot is the total number of independent movements it can make. Humanoid robots are **high-DoF** systems, often having 20 to 50+ DoF. This incredible mobility also makes them incredibly complex to control.

### Kinematic Chains in Humanoids

A humanoid robot can be viewed as a collection of interconnected **kinematic chains**.
*   Each leg is a kinematic chain from the hip to the foot.
*   Each arm is a kinematic chain from the shoulder to the hand.
*   The entire body is a "floating base" kinematic chain, where the torso's position is not fixed.

Controlling a humanoid requires **whole-body control**, which means coordinating the motion of all these kinematic chains simultaneously to achieve a task (e.g., walking) while maintaining balance.

### The Key to Balance: The Zero Moment Point (ZMP)

How does a humanoid robot (or a human) stay balanced while walking? The key concept is the **Zero Moment Point (ZMP)**.

*   **Definition:** The ZMP is a point on the ground where the net moment (or torque) due to gravity and the robot's inertial forces is zero.
*   **Intuitive Explanation:** It's the point on the ground where the total "tipping-over" torque is zero. If you imagine all the forces acting on the robot being summarized as a single point of pressure on the ground, that point is the ZMP.
*   **The Rule of Balance:** For the robot to remain stable, the **ZMP must stay within the support polygon**.
    *   **Support Polygon:** The area on the ground enclosed by the robot's contact points (i.e., its feet). When standing on two feet, it's the area spanning both feet. When on one foot, it's just the area of that foot.

    ![ZMP and Support Polygon](https://i.imgur.com/gKkR5aF.png)
    *Figure 1: For a humanoid to be stable, its Zero Moment Point (ZMP) must remain within the support polygon formed by its feet.*

To walk, a humanoid robot's controller must constantly plan a trajectory for the robot's center of mass (CoM) such that the resulting ZMP stays within the support polygon as it shifts from one foot to the other.

## Practical Section

In this exercise, we will model a very simple humanoid robot in PyBullet. We will then write a function to calculate the ZMP for our robot in a static pose. This will provide a concrete understanding of this crucial concept in bipedal stability.

### The Code

Create a new Python file named `humanoid_zmp.py`.

The script will:
1.  Programmatically create a simple humanoid model composed of basic shapes (cubes for torso, legs, etc.).
2.  Define a function `calculate_zmp` that takes the robot's model and calculates the ZMP based on the contact forces with the ground.
3.  Hold the robot in a static pose and print the calculated ZMP.

```python title="humanoid_zmp.py"
import pybullet as p
import time
import pybullet_data
import numpy as np

# -- Setup --
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.setRealTimeSimulation(0)

planeId = p.loadURDF("plane.urdf")

# -- Create a Simple Humanoid Model --
def create_humanoid():
    # Define shapes
    torso_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.1, 0.15, 0.25])
    leg_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.2])
    foot_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, 0.1, 0.02])

    # Create the torso (base)
    torso_id = p.createMultiBody(baseMass=2, baseCollisionShapeIndex=torso_shape, basePosition=[0, 0, 0.8])
    
    # Create left leg and foot
    left_leg_id = p.createMultiBody(baseMass=1, baseCollisionShapeIndex=leg_shape, basePosition=[-0.15, 0, 0.5])
    left_foot_id = p.createMultiBody(baseMass=0.5, baseCollisionShapeIndex=foot_shape, basePosition=[-0.15, 0, 0.29])

    # Create right leg and foot
    right_leg_id = p.createMultiBody(baseMass=1, baseCollisionShapeIndex=leg_shape, basePosition=[0.15, 0, 0.5])
    right_foot_id = p.createMultiBody(baseMass=0.5, baseCollisionShapeIndex=foot_shape, basePosition=[0.15, 0, 0.29])

    # Connect parts with joints (simplified fixed joints for this demo)
    p.createConstraint(torso_id, -1, left_leg_id, -1, p.JOINT_FIXED, [0,0,0], [0,0,0.25], [-0.15,0,0.3])
    p.createConstraint(left_leg_id, -1, left_foot_id, -1, p.JOINT_FIXED, [0,0,0], [0,0,-0.2], [0,0,0.02])
    p.createConstraint(torso_id, -1, right_leg_id, -1, p.JOINT_FIXED, [0,0,0], [0,0,0.25], [0.15,0,0.3])
    p.createConstraint(right_leg_id, -1, right_foot_id, -1, p.JOINT_FIXED, [0,0,0], [0,0,-0.2], [0,0,0.02])
    
    return [left_foot_id, right_foot_id] # Return the feet IDs for contact checking

# -- ZMP Calculation --
def calculate_zmp(robot_feet_ids, plane_id):
    """
    Calculates the Zero Moment Point (ZMP) based on ground contact forces.
    """
    contact_points = p.getContactPoints(bodyA=planeId)
    
    if not contact_points:
        return None

    # ZMP formula: zmp_x = sum(P_i.x * F_i.z) / sum(F_i.z)
    # where P_i is the contact point and F_i is the contact force
    numerator_x, numerator_y, denominator = 0.0, 0.0, 0.0
    
    for point in contact_points:
        # Check if the contact involves one of the robot's feet
        if point[2] in robot_feet_ids:
            contact_pos = point[5] # Contact position on body A (the plane)
            normal_force = point[9] # Normal force
            
            if normal_force > 0:
                numerator_x += contact_pos[0] * normal_force
                numerator_y += contact_pos[1] * normal_force
                denominator += normal_force
    
    if denominator > 0:
        zmp_x = numerator_x / denominator
        zmp_y = numerator_y / denominator
        return np.array([zmp_x, zmp_y, 0])
    else:
        return None

# -- Main Simulation --
feet = create_humanoid()

print("Simulating static pose and calculating ZMP...")

# Let the simulation settle
for _ in range(240):
    p.stepSimulation()
    time.sleep(1./240.)

# Calculate ZMP in the static pose
zmp = calculate_zmp(feet, planeId)

if zmp is not None:
    print(f"\nCalculated ZMP at (x, y): ({zmp[0]:.4f}, {zmp[1]:.4f})")
    # Visualize the ZMP with a small sphere
    p.createVisualShape(p.GEOM_SPHERE, radius=0.02, rgbaColor=[1,0,0,1])
    p.createMultiBody(baseVisualShapeIndex=-1, basePosition=zmp)
    p.addUserDebugText("ZMP", zmp + np.array([0,0,0.1]), [1,0,0], 1.2)
else:
    print("\nRobot is not in contact with the ground. Cannot calculate ZMP.")

print("\nSimulation will run for 10 seconds.")
for _ in range(240 * 10):
    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()
```

### Running the Code

Run the script from your terminal: `python humanoid_zmp.py`.

A simple humanoid model made of blocks will appear in the simulation. After a moment, the script will calculate and print the position of the ZMP. You will also see a small **red sphere** appear on the ground plane between the robot's feet, visually representing the ZMP's location.

Since the robot is standing still and symmetrically, the ZMP should be at `(0, 0)`, exactly between its feet and in the center of its support polygon. This indicates a stable pose.

## Self-Assessment

1.  What is a major reason for designing robots with a humanoid form?
2.  What does "Degrees of Freedom" (DoF) refer to in a robot?
3.  What is the "support polygon" for a humanoid robot standing on one foot?
4.  What is the fundamental rule for maintaining balance, expressed in terms of the ZMP?
5.  In our `calculate_zmp` function, why do we use `normal_force` as the weighting factor for the contact positions?

---

**Answer Key:**

1.  A major reason is to enable robots to operate effectively in **human-centric environments**, using tools and navigating spaces designed for humans.
2.  Degrees of Freedom (DoF) refers to the total number of **independent movements** a robot can make.
3.  The support polygon for a humanoid standing on one foot is the **area of the sole of that foot**.
4.  For the robot to remain stable, its **Zero Moment Point (ZMP) must stay within its support polygon**.
5.  The ZMP calculation is a weighted average of the contact points. The `normal_force` represents the magnitude of the pressure at each contact point, so it is the correct physical quantity to use as the weighting factor. Points with more pressure contribute more to the final ZMP location.

## Further Reading

*   [Boston Dynamics: Atlas](https://www.youtube.com/watch?v=tF4DML7FIWk) - See one of the world's most advanced humanoid robots in action.
*   [ZMP and Humanoid Walking](https://www.youtube.com/watch?v=jGAqa8s_l2k) - A more technical but clear video explanation of ZMP.
*   [Humanoid Robotics Overview](https://www.cs.cmu.edu/~cga/humanoids/) - Lecture notes from CMU's humanoid robotics course.
*   *Springer Handbook of Robotics, Part C: Humanoid Robots* - A comprehensive (and advanced) reference on the topic.
