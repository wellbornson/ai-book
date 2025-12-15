--- 
title: "Lesson 8.3: Pick-and-Place and Task Sequencing"
sidebar_position: 3
description: "Bring it all together by programming a complete pick-and-place task, learning how to decompose complex tasks into sequences of simpler actions."
tags: [manipulation, pick-and-place, task-sequencing, state-machine]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Decompose a complex manipulation task like "pick and place" into a sequence of simpler sub-tasks.
*   Implement a state machine to manage the execution of a task sequence.
*   Coordinate perception, motion planning, and gripper control to achieve a goal.
*   Understand basic strategies for error detection and recovery in manipulation.
*   Program a full pick-and-place pipeline for a robot arm in PyBullet.

## Prerequisites

*   [Lesson 8.2: Grasp Planning and Execution](./lesson-02-grasp-planning-and-execution.md)
*   [Lesson 5.1: Introduction to Feedback Control](../chapter-05-control-systems/lesson-01-introduction-to-feedback-control.md) (State Machines)
*   [Lesson 4.2: Inverse Kinematics and Solutions](../chapter-04-kinematics-and-dynamics/lesson-02-inverse-kinematics-and-solutions.md)

## Theory Section

### From Simple Actions to Complex Tasks

So far, we've learned about the individual building blocks of robotics: kinematics, control, perception, and grasp planning. A **pick-and-place operation** is the classic robotics task that brings all of these components together. It's the foundation for a huge range of applications, from warehouse automation to manufacturing and assembly.

Successfully programming a pick-and-place task requires moving beyond single commands and thinking in terms of **task sequencing**.

### Task Decomposition

A seemingly simple instruction like "move the blue block to the red bin" must be broken down into a precise sequence of primitive actions. A typical pick-and-place task can be decomposed as follows:

1.  **START:** The robot is in a known, safe "home" position.
2.  **DETECT_OBJECT:** Use perception (e.g., a camera and object detection) to find the target object's position.
3.  **PLAN_GRASP:** Determine a suitable grasp pose for the object.
4.  **MOVE_TO_PRE_GRASP:** Move the arm to a safe approach pose above the object.
5.  **APPROACH:** Move the gripper linearly down to the grasp pose.
6.  **GRASP:** Close the gripper to secure the object.
7.  **LIFT:** Move the arm vertically upwards to clear any nearby obstacles.
8.  **MOVE_TO_PRE_PLACE:** Move the arm to a safe approach pose above the destination (the "place" location).
9.  **DESCEND:** Move the gripper linearly down to the place pose.
10. **RELEASE:** Open the gripper to release the object.
11. **RETREAT:** Move the arm vertically upwards.
12. **RETURN_HOME:** Move the arm back to its home position.

This sequence can be effectively managed using a **State Machine**, where each step is a state, and the transition to the next state occurs upon successful completion of the current one.

![Pick and Place State Machine](https://i.imgur.com/gKkR5aF.png)
*Figure 1: A simplified state machine diagram for a pick-and-place task.*

### Coordinating Perception and Action

A key challenge is coordinating perception with manipulation. The robot cannot plan its grasp or its arm movements until it has successfully detected the object.

*   **Open-Loop vs. Closed-Loop Execution:**
    *   **Open-Loop:** The robot detects the object once at the beginning and then executes the entire motion sequence blindly. This is fast but will fail if the object moves or the initial perception was inaccurate.
    *   **Closed-Loop (Visual Servoing):** The robot continuously uses its camera to update the object's position and adjust its arm trajectory in real-time. This is more robust but also much more complex.

For many structured tasks, a "detect-then-act" open-loop approach is sufficient.

### Error Detection and Recovery

What happens if something goes wrong? A robust system must have strategies for error detection and recovery.

*   **Error Detection:**
    *   **Grasp Failure:** After lifting, check if the object is still in the gripper. This can be done with a force sensor, a camera, or by checking if the gripper fingers are fully closed (which would imply nothing is between them).
    *   **Motion Planning Failure:** The IK solver fails to find a solution to reach a target pose.
    *   **Collision:** A force sensor or motor current sensor detects an unexpected spike in force.

*   **Recovery Strategies:**
    *   **Retry:** Attempt the failed action again (e.g., re-plan the grasp).
    *   **Re-scan:** Re-run the object detection routine to get an updated object pose.
    *   **Abort:** If the error is unrecoverable, move to a safe home position and signal for human assistance.

## Practical Section

In this final exercise of the chapter, we will implement a complete, albeit simplified, pick-and-place state machine in PyBullet. We will combine our knowledge of IK, gripper control, and task sequencing to make a KUKA arm pick up a block and place it in a target location.

### The Code

Create a new Python file named `pick_and_place.py`.

This script is more complex than previous ones. It defines a `RobotController` class that manages the robot's state and encapsulates functions for moving the arm and controlling the gripper. The main loop is a state machine that progresses through the pick-and-place sequence.

```python title="pick_and_place.py"
import pybullet as p
import time
import pybullet_data
import numpy as np

# --- Setup ---
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -10)
p.setRealTimeSimulation(0)

# Load environment
p.loadURDF("plane.urdf")
table_id = p.loadURDF("table/table.urdf", useFixedBase=True)
robot_id = p.loadURDF("kuka_lbr_iiwa/model_vr_with_gripper.urdf", basePosition=[0,0,0.625], useFixedBase=True)
object_id = p.loadURDF("cube_small.urdf", basePosition=[0.5, 0, 0.7])

# Robot parameters
num_joints = p.getNumJoints(robot_id)
end_effector_link_index = 6
gripper_joints = [8, 10]

class RobotController:
    def __init__(self, robot_id):
        self.robot_id = robot_id
        self.home_pose = [0] * num_joints # Simplified home pose
        self.state = "START"
        self.target_object_pos = None
        self.place_target_pos = None

    def move_to(self, target_pos, target_ori=None, duration=2.0):
        """Moves the end-effector to a target pose and waits."""
        if target_ori is None:
            # Default orientation: pointing down
            target_ori = p.getQuaternionFromEuler([0, -np.pi, 0])
        
        joint_angles = p.calculateInverseKinematics(
            self.robot_id, end_effector_link_index, target_pos, target_ori
        )
        
        p.setJointMotorControlArray(
            self.robot_id,
            range(num_joints),
            p.POSITION_CONTROL,
            targetPositions=joint_angles,
            forces=[500]*num_joints
        )
        
        start_time = time.time()
        while time.time() - start_time < duration:
            p.stepSimulation()
            time.sleep(1./240.)

    def control_gripper(self, open_gripper=True, duration=1.0):
        """Opens or closes the gripper."""
        target_pos = 0.1 if open_gripper else 0.01
        p.setJointMotorControl2(self.robot_id, gripper_joints[0], p.POSITION_CONTROL, targetPosition=target_pos, force=50)
        p.setJointMotorControl2(self.robot_id, gripper_joints[1], p.POSITION_CONTROL, targetPosition=-target_pos, force=50)
        
        start_time = time.time()
        while time.time() - start_time < duration:
            p.stepSimulation()
            time.sleep(1./240.)

# --- Main State Machine Loop ---
robot = RobotController(robot_id)
robot.place_target_pos = np.array([-0.5, 0, 0.7]) # Define a place location

print("--- Starting Pick-and-Place Task ---")

try:
    while True:
        p.stepSimulation()
        time.sleep(1./240.)

        current_state = robot.state
        print(f"Current State: {current_state}")

        if current_state == "START":
            # Start by opening the gripper and moving to a safe home pose
            robot.control_gripper(open_gripper=True)
            robot.move_to([0.4, 0, 1.0]) # Home pose
            robot.state = "DETECT_OBJECT"

        elif current_state == "DETECT_OBJECT":
            # In a real system, this would use a camera. Here, we just get the known position.
            obj_pos, _ = p.getBasePositionAndOrientation(object_id)
            robot.target_object_pos = np.array(obj_pos)
            print(f"  Object detected at {robot.target_object_pos}")
            robot.state = "MOVE_TO_PRE_GRASP"

        elif current_state == "MOVE_TO_PRE_GRASP":
            # Move to a safe position above the object
            pre_grasp_pos = robot.target_object_pos + np.array([0, 0, 0.2])
            robot.move_to(pre_grasp_pos)
            robot.state = "APPROACH"

        elif current_state == "APPROACH":
            # Move down to the object
            robot.move_to(robot.target_object_pos)
            robot.state = "GRASP"
            
        elif current_state == "GRASP":
            robot.control_gripper(open_gripper=False)
            robot.state = "LIFT"

        elif current_state == "LIFT":
            lift_pos = robot.target_object_pos + np.array([0, 0, 0.2])
            robot.move_to(lift_pos)
            robot.state = "MOVE_TO_PRE_PLACE"

        elif current_state == "MOVE_TO_PRE_PLACE":
            pre_place_pos = robot.place_target_pos + np.array([0, 0, 0.2])
            robot.move_to(pre_place_pos)
            robot.state = "DESCEND"

        elif current_state == "DESCEND":
            robot.move_to(robot.place_target_pos)
            robot.state = "RELEASE"

        elif current_state == "RELEASE":
            robot.control_gripper(open_gripper=True)
            robot.state = "RETREAT"
            
        elif current_state == "RETREAT":
            retreat_pos = robot.place_target_pos + np.array([0, 0, 0.2])
            robot.move_to(retreat_pos)
            robot.state = "RETURN_HOME"

        elif current_state == "RETURN_HOME":
            robot.move_to([0.4, 0, 1.0]) # Home pose
            robot.state = "DONE"

        elif current_state == "DONE":
            print("\n--- Pick-and-Place Task Complete ---")
            break

except KeyboardInterrupt:
    print("Simulation interrupted.")
finally:
    time.sleep(5)
    p.disconnect()
```

### Running the Code

Run the script from your terminal: `python pick_and_place.py`.

You will see the KUKA robot arm execute the full pick-and-place sequence. The terminal will print the current state of the state machine as it progresses through the task. The robot will:
1.  Move to a starting "home" position.
2.  Move to a pre-grasp position above the cube.
3.  Descend and grasp the cube.
4.  Lift the cube.
5.  Move to a pre-place position above the target destination.
6.  Descend and release the cube.
7.  Retreat and return to its home position.

Congratulations! You have programmed a complete, end-to-end robotics task.

## Self-Assessment

1.  What is "task decomposition" in the context of robotics?
2.  Why is a state machine a good programming pattern for managing a pick-and-place task?
3.  What is the purpose of the `LIFT` state in our sequence, right after `GRASP`?
4.  What is a potential failure point in our `pick_and_place.py` script, and how might you detect it in a more robust system?
5.  What is the difference between an "open-loop" and "closed-loop" pick-and-place execution?

--- 

**Answer Key:**

1.  Task decomposition is the process of breaking down a high-level, complex task (like "clean the kitchen") into a sequence of smaller, simpler, and more manageable sub-tasks or primitive actions (like "pick up sponge," "move to sink," etc.).
2.  A state machine is a good pattern because it provides a clear, structured, and easy-to-debug way to manage the sequence of operations. Each state represents a distinct action, and the transitions between states are well-defined, making the overall logic easy to follow.
3.  The `LIFT` state is crucial because it ensures the robot lifts the object vertically off the surface before attempting to move it horizontally. This prevents the robot from dragging the object across the table, which could knock over other objects or cause the grasp to fail.
4.  A potential failure is if the grasp fails and the robot drops the block. In our simple script, the robot would continue the sequence blindly. A more robust system could detect this by using a camera to verify the block is still in the gripper after the `LIFT` state, or by checking if the gripper fingers are fully closed (indicating no object is present).
5.  Our script is **open-loop** because it detects the object's position once and then executes the rest of the motion sequence based on that initial information. A **closed-loop** execution would continuously use sensors (like a camera) to track the object and the gripper, making real-time corrections throughout the entire motion.

## Further Reading

*   [ROS State Machines in Python](http://wiki.ros.org/smach/Tutorials/Getting%20Started) - A look at how state machines are implemented in the Robot Operating System (ROS).
*   *Robot Programming by Demonstration* - A field of study focusing on teaching robots complex tasks through demonstration, which heavily relies on task sequencing.
*   [Behavior Trees for AI: How They Work](https://www.youtube.com/watch?v=n6iF-buT3_c) - An introduction to Behavior Trees, another powerful alternative to state machines for sequencing complex AI behavior.
