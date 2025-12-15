--- 
title: "Lesson 10.1: System Integration and Architecture"
sidebar_position: 1
description: "Learn how complex robotic systems are built by exploring software architecture, modularity, inter-process communication, and the Robot Operating System (ROS)."
tags: [integration, architecture, ros, software-engineering, modularity]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Explain the importance of a structured software architecture in robotics.
*   Describe the core concepts of the Robot Operating System (ROS): nodes, topics, and messages.
*   Understand the benefits of modularity and inter-process communication.
*   Outline how the perception-planning-control loops are coordinated in a real system.
*   Implement a simple multi-component system in Python that mimics a ROS-like architecture.

## Prerequisites

*   [Lesson 8.3: Pick-and-Place and Task Sequencing](../chapter-08-manipulation/lesson-03-pick-and-place-and-task-sequencing.md) (Understanding of task sequencing)
*   General programming knowledge (functions, classes, basic data structures).

## Theory Section

### Putting It All Together: From Components to System

Throughout this course, we have explored the individual "organs" of a robot: the senses (perception), the brain (planning and control), and the muscles (actuation). But a robot, like a living organism, is more than the sum of its parts. **System integration** is the process of assembling these individual components into a single, cohesive, and functional system.

A well-designed **software architecture** is the blueprint that dictates how these components are organized and how they communicate with each other. A good architecture makes a system easier to build, debug, test, and upgrade. A poor architecture leads to a "brittle" system that is difficult to understand and maintain.

### The Need for Modularity

A complex robot cannot be written as a single, monolithic program. Instead, we use **modularity**. The system is broken down into smaller, independent, and interchangeable modules (or "processes"). Each module has a specific responsibility:

*   A **camera module** might be responsible for capturing images.
*   A **perception module** might take those images and detect objects.
*   A **planning module** might take the object locations and plan a path for an arm.
*   A **control module** might take the path and generate motor commands.

These modules run as separate processes that communicate with each other. This has several advantages:
*   **Decoupling:** A bug in the perception module won't crash the motor control module.
*   **Reusability:** A well-written camera module can be reused on many different robots.
*   **Scalability:** Different modules can be run on different computers for better performance.
*   **Teamwork:** Different teams of engineers can work on different modules simultaneously.

### The Robot Operating System (ROS)

How do these independent modules talk to each other? This is where a **middleware** framework comes in. The most popular middleware in robotics is the **Robot Operating System (ROS)**.

Despite its name, ROS is *not* an operating system like Windows or Linux. It is a flexible framework and set of tools for writing robot software. It provides a structured communication layer that allows different modules to exchange information seamlessly.

#### Core ROS Concepts:

1.  **Nodes:** A node is a single process (a module in our system). A ROS system is composed of many nodes. For example, you might have a `/camera_driver` node, a `/object_detector` node, and an `/arm_controller` node.

2.  **Topics & Messages:** Nodes communicate with each other by publishing and subscribing to **topics**.
    *   A **topic** is a named bus, like a channel, over which data flows. For example, the `/camera_driver` node might publish images to an `/camera/image_raw` topic.
    *   A **message** is the data structure that is sent on a topic. ROS has standard message types for common data like images (`sensor_msgs/Image`), laser scans (`sensor_msgs/LaserScan`), and robot poses (`geometry_msgs/Pose`).

3.  **Publish/Subscribe Model:** This is the primary communication method.
    *   A node can **publish** messages to a topic (e.g., the camera node publishes images).
    *   Other nodes can **subscribe** to that topic to receive the messages (e.g., the object detector subscribes to the images).
    *   The publisher and subscriber don't need to know about each other's existence. They only need to agree on the topic name and message type. This makes the system extremely flexible and decoupled.

    ![ROS Publish/Subscribe Model](https://i.imgur.com/gKkR5aF.png)
    *Figure 1: In ROS, Node 1 publishes messages to a Topic, and Node 2 and Node 3 can subscribe to that topic to receive the data without direct knowledge of Node 1.*

### Coordinating the Perception-Planning-Control Loop

Using a ROS-like architecture, we can see how the full pick-and-place task from the previous chapter would be orchestrated:

1.  A `/camera_node` publishes images to the `/camera/image` topic.
2.  A `/perception_node` subscribes to `/camera/image`. When it receives an image, it detects the object and publishes the object's pose to an `/object/pose` topic.
3.  A `/task_planner_node` (our state machine) subscribes to `/object/pose`. Upon receiving the pose, it plans the grasp and the arm trajectory. It then starts publishing a series of target poses to an `/arm/target_pose` topic.
4.  An `/arm_controller_node` subscribes to `/arm/target_pose`. For each target pose it receives, it calculates the required joint angles (using IK) and sends low-level commands to the robot's motors. It might also publish the arm's current state to an `/arm/current_state` topic for monitoring.

### Real-Time Considerations

Robotics often involves **real-time systems**, where computations must be completed within a strict deadline. If a control loop for a balancing robot doesn't run fast enough, the robot will fall.

Architectures like ROS help, but they are not "hard" real-time by default. A message could be delayed. Designing robust, real-time robotic systems requires careful consideration of scheduling, process priorities, and communication overhead. Often, the lowest-level control loops (like motor PID controllers) are run on dedicated microcontrollers that guarantee timing, while higher-level planning runs on a less time-critical computer.

## Practical Section

Installing ROS is a major undertaking. For this exercise, we will instead create a simplified, conceptual implementation of a ROS-like architecture in Python. We will build a system with three "nodes" (as classes) that communicate through a central "message bus" (a simple dictionary) to perform a task.

Our task: A "perception" node will identify a target's location. A "planner" node will decide where the robot should move. A "controller" node will execute the movement in PyBullet.

### The Code

Create a new Python file named `simple_ros_like_system.py`.

The script defines three classes: `PerceptionNode`, `PlannerNode`, and `ControllerNode`. They all share a `message_bus` dictionary. The main loop calls the `update()` method of each "node" in turn, simulating how a real multi-process system would operate.

``` title="simple_ros_like_system.py"
import pybullet as p
import time
import pybullet_data
import numpy as np

# --- Message Bus (A simple dictionary to act as our ROS topics) ---
message_bus = {
    "object_pose": None,
    "robot_target_velocity": None,
}

# --- Node 1: Perception ---
class PerceptionNode:
    def __init__(self, object_id):
        self.object_id = object_id

    def update(self):
        # In a real system, this would process camera images.
        # Here, we just get the ground truth from the simulation.
        obj_pos, _ = p.getBasePositionAndOrientation(self.object_id)
        
        # "Publish" the message
        message_bus["object_pose"] = np.array(obj_pos)
        # print(f"[Perception] Published object pose: {message_bus['object_pose']}")

# --- Node 2: Planner ---
class PlannerNode:
    def __init__(self, robot_id):
        self.robot_id = robot_id
        self.goal_reached = False

    def update(self):
        # "Subscribe" to the object_pose topic
        object_pose = message_bus["object_pose"]
        
        if object_pose is None or self.goal_reached:
            # "Publish" a stop command if no object or goal is reached
            message_bus["robot_target_velocity"] = (0, 0)
            return

        robot_pos, robot_ori = p.getBasePositionAndOrientation(self.robot_id)
        robot_yaw = p.getEulerFromQuaternion(robot_ori)[2]
        
        # Plan: Calculate desired linear and angular velocity to reach the object
        vector_to_target = object_pose[:2] - np.array(robot_pos[:2])
        distance_to_target = np.linalg.norm(vector_to_target)

        if distance_to_target < 0.3:
            print("[Planner] Goal reached!")
            self.goal_reached = True
            message_bus["robot_target_velocity"] = (0, 0)
            return

        target_yaw = np.arctan2(vector_to_target[1], vector_to_target[0])
        yaw_error = target_yaw - robot_yaw
        yaw_error = np.arctan2(np.sin(yaw_error), np.cos(yaw_error))

        # Simple P-controller for planning
        v_linear = 0.5 * distance_to_target
        omega_angular = 1.0 * yaw_error
        
        # "Publish" the planned velocities
        message_bus["robot_target_velocity"] = (v_linear, omega_angular)
        # print(f"[Planner] Publishing target velocity: ({v_linear:.2f}, {omega_angular:.2f})")


# --- Node 3: Controller ---
class ControllerNode:
    def __init__(self, robot_id, wheel_indices, wheel_radius, wheel_base):
        self.robot_id = robot_id
        self.wheel_indices = wheel_indices
        self.wheel_radius = wheel_radius
        self.wheel_base = wheel_base

    def update(self):
        # "Subscribe" to the robot_target_velocity topic
        target_vel = message_bus["robot_target_velocity"]
        
        if target_vel is None:
            return
            
        v_linear, omega_angular = target_vel
        
        # Convert linear/angular vel to wheel vel (kinematics)
        v_left = v_linear - (omega_angular * self.wheel_base / 2)
        v_right = v_linear + (omega_angular * self.wheel_base / 2)
        
        target_left_ang_vel = v_left / self.wheel_radius
        target_right_ang_vel = v_right / self.wheel_radius
        
        # Send commands to motors
        p.setJointMotorControl2(
            self.robot_id, self.wheel_indices[0], p.VELOCITY_CONTROL, 
            targetVelocity=target_left_ang_vel, force=100
        )
        p.setJointMotorControl2(
            self.robot_id, self.wheel_indices[1], p.VELOCITY_CONTROL, 
            targetVelocity=target_right_ang_vel, force=100
        )

# --- Main Simulation ---
if __name__ == "__main__":
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -10)
    
    p.loadURDF("plane.urdf")
    robot_id = p.loadURDF("racecar/racecar.urdf", basePosition=[0, 0, 0.1])
    object_id = p.loadURDF("cube_small.urdf", basePosition=[3, 1, 0.05])
    
    # Instantiate our "nodes"
    perception_node = PerceptionNode(object_id)
    planner_node = PlannerNode(robot_id)
    controller_node = ControllerNode(
        robot_id=robot_id, 
        wheel_indices=[5, 7], # Rear wheels
        wheel_radius=0.1, 
        wheel_base=0.5
    )
    
    print("--- Starting ROS-like System Simulation ---")
    
    try:
        while not planner_node.goal_reached:
            # In a real system, these would be separate processes running in parallel.
            # Here, we call them sequentially to simulate the data flow.
            perception_node.update()
            planner_node.update()
            controller_node.update()
            
            p.stepSimulation()
            time.sleep(1./240.)
            
    except KeyboardInterrupt:
        print("Simulation interrupted.")
    finally:
        print("\nSimulation finished.")
        p.disconnect()
```

### Running the Code

Run the script from your terminal: `python simple_ros_like_system.py`.

You will see the racecar drive towards the cube. Although this is a single script, it's structured into three distinct classes (nodes), each with a single responsibility, and they only communicate via the shared `message_bus`.

*   The **PerceptionNode** "sees" the cube and "publishes" its pose.
*   The **PlannerNode** "subscribes" to the pose and "publishes" a desired velocity.
*   The **ControllerNode** "subscribes" to the velocity and sets the motor speeds.

This demonstrates the power and flexibility of a modular, message-passing architecture, which is the foundation of modern robotics software engineering.

## Self-Assessment

1.  What is a major advantage of a modular software architecture over a monolithic one?
2.  In the ROS publish/subscribe model, do the publisher and subscriber nodes need to know about each other directly?
3.  What are the three core concepts of ROS discussed in this lesson?
4.  Why are "real-time" considerations important in robotics?
5.  In our `simple_ros_like_system.py` script, what acts as our "middleware" or communication layer?

--- 

**Answer Key:**

1.  A major advantage of modularity is **decoupling**. It allows different components to be developed, tested, and run independently, making the system more robust, reusable, and easier to manage.
2.  No, they do not. They only need to agree on the **topic name** and the **message type**, which makes the system highly flexible.
3.  The three core concepts are **Nodes** (processes), **Topics** (named communication channels), and **Messages** (the data sent on topics).
4.  Real-time considerations are important because many robotics tasks (like balancing or fast manipulation) require computations and control actions to be completed within strict deadlines to ensure stability and safety.
5.  The shared Python dictionary named `message_bus` acts as our simplified middleware. The keys of the dictionary are like "topic names," and the values are the "messages."

## Further Reading

*   [ROS Tutorials](http://wiki.ros.org/ROS/Tutorials) - The official tutorials for learning ROS.
*   [What is ROS?](https://www.youtube.com/watch?v=kYJru4A3t5o) - A high-level video introduction.
*   *A Systematic Approach to Learning Robot Programming with ROS* by Wyatt Newman - A textbook for learning ROS in a structured way.
*   [Micro-ROS](https://micro.ros.org/) - An introduction to running ROS on microcontrollers, highlighting the separation of high-level and low-level control.
