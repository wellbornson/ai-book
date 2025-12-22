---
title: "Lesson 5.1: Introduction to Feedback Control"
sidebar_position: 1
description: "Explore the fundamental concepts of feedback control, differentiating between open-loop and closed-loop systems, and understanding their importance in robotics."
tags: [control-systems, feedback-control, open-loop, closed-loop]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Differentiate between open-loop and closed-loop (feedback) control systems.
*   Identify the key components of a typical feedback control loop.
*   Explain the advantages of feedback control in robotics.
*   Recognize real-world examples of both open-loop and closed-loop control systems.
*   Understand the basic principle of how a robot uses feedback to achieve its goals.

## Prerequisites

*   [Lesson 3.2: Motor Control and PWM](../chapter-03-actuators-and-control/lesson-02-motor-control-and-pwm.md) (Basic understanding of motor control)

## Theory Section

### Taking Control: The Robot's Brain and Body

In previous lessons, we've explored how robots perceive the world (sensors) and how they act upon it (actuators). Now, we delve into the "brain" of the robot: the **control system**. The control system is the part of the robot that makes decisions and translates high-level goals into specific actuator commands.

At its core, a control system's job is to ensure that a robot (or any system) behaves in a desired way, even in the face of disturbances and uncertainties.

### Open-Loop vs. Closed-Loop Control

There are two fundamental types of control systems:

#### 1. Open-Loop Control

An **open-loop control system** issues commands to an actuator without using any feedback from sensors to verify if the command was executed correctly. It assumes that the actuator will always perform as expected.

*   **How it works:** `Controller` -> `Actuator` -> `Process`
*   **Example 1: A Toaster.** You set a timer for "light toast," and the toaster heats for a fixed duration. It doesn't measure the actual toast browning. If you put in frozen bread, it might come out too light.
*   **Example 2: Simple Traffic Light.** A traffic light operates on a fixed timing sequence. It doesn't detect traffic queues or accidents.
*   **In Robotics:** Sending a fixed PWM duty cycle to a DC motor without checking its actual speed.

    ![Open-Loop Control](https://i.imgur.com/gL2jI7f.png)
    *Figure 1: Diagram of an open-loop control system. There is no feedback from the process to the controller.*

*   **Advantages:** Simple, inexpensive to implement, no sensor required.
*   **Disadvantages:** Inaccurate, cannot compensate for disturbances, highly sensitive to changes in the environment or system properties.

#### 2. Closed-Loop Control (Feedback Control)

A **closed-loop control system**, also known as a **feedback control system**, constantly measures the actual state of the system using sensors and compares it to the desired state (the "setpoint"). It then calculates an error and adjusts the actuator commands to reduce that error.

*   **How it works:** `Controller` -> `Actuator` -> `Process` -> `Sensor` -> `Feedback` -> `Controller`
*   **Example 1: Cruise Control in a Car.** You set a desired speed (setpoint). The car measures its actual speed (sensor). If actual speed is too low, it increases engine power (actuator). If too high, it reduces power. It compensates for hills and wind.
*   **Example 2: A Home Thermostat.** You set a desired temperature. The thermostat measures the room's actual temperature. If it's too cold, it turns on the heater.
*   **In Robotics:** A servo motor using an internal position sensor to ensure it reaches and holds a specific angle.

    ![Closed-Loop Control](https://i.imgur.com/w9cQf3E.png)
    *Figure 2: Diagram of a closed-loop (feedback) control system. The sensor provides feedback to the controller, allowing it to correct errors.*

*   **Advantages:** Accurate, robust to disturbances, can compensate for system variations, can achieve stability.
*   **Disadvantages:** More complex, requires sensors, can be unstable if not designed and tuned correctly.

### Components of a Feedback Control Loop

A typical feedback control system has four main components:

1.  **Setpoint (Desired State):** The target value the system aims to achieve (e.g., desired robot position, desired motor speed, desired temperature).
2.  **Process (Plant):** The system being controlled (e.g., the robot arm, the motor, the room).
3.  **Sensor:** Measures the actual state of the process (e.g., encoder for motor speed, camera for robot position, thermometer for temperature).
4.  **Controller:** The "brain" that compares the setpoint to the measured actual state, calculates the error, and generates a control command for the actuator to reduce that error.

    *   `Error = Setpoint - Measured Value`

### The Importance of Control in Robotics

Feedback control is absolutely fundamental to robotics. Without it, robots could not:
*   **Hold a position:** A robot arm would just flop down due to gravity.
*   **Drive in a straight line:** Small wheel speed differences would make it curve.
*   **Grasp objects firmly:** It wouldn't know how much pressure to apply.
*   **Balance:** A bipedal robot would fall immediately.

Effective control systems allow robots to execute complex tasks reliably, precisely, and robustly in uncertain environments.

## Practical Section

In this conceptual exercise, we'll think about how to turn an open-loop robotic movement into a closed-loop one. We'll revisit the task of driving a robot a specific distance.

### Exercise: Designing a Closed-Loop Drive System

Imagine you have a simple differential drive robot with:
*   Two DC motors for the wheels.
*   Wheel encoders on each wheel to measure rotation.
*   A microcontroller that can send PWM signals to an H-Bridge motor driver.

Your goal is to make the robot drive exactly 1 meter forward, stop, and hold its position, regardless of the surface (e.g., carpet, hardwood, a slight incline).

**Answer the following questions, considering the components of a closed-loop system:**

1.  **Setpoint:** What is the setpoint for this task?
2.  **Process:** What is the "process" being controlled?
3.  **Sensor:** What sensor would you use, and what information would it provide?
4.  **Controller Input:** What information does your controller need to make a decision?
5.  **Controller Output:** What command would your controller send to the actuators?
6.  **Feedback Loop:** Describe how the error is calculated and how the system corrects itself to reach the target distance.

## Code Examples

No new code will be written in this lesson, as it is foundational theory. However, the conceptual "Hello, Robot!" code from Lesson 1.3 provides a basic illustration of the interaction between `sense` (sensor) and `act` (actuator), which forms the basis of a control loop.

```python title="conceptual_control_loop.py"
# Conceptual "Hello, Robot!" (revisited)

# 1. Connect to the robot's systems
robot = connect_to_robot("my_simulated_robot")

# 2. Get Setpoint (Desired state)
desired_position = 1.0 # meters

# 3. Sense (Measure actual state)
current_position = robot.get_current_position_from_sensors() # e.g., using odometry from encoders

# 4. Control (Calculate error and command)
error = desired_position - current_position

# This is a very simplified controller:
if error > 0.1: # If far from target
    robot.move_forward(speed=0.5) # Actuate
elif error < -0.1: # If overshoot
    robot.move_backward(speed=0.2) # Actuate
else: # If close enough
    robot.stop() # Actuate

# This loop would repeat constantly, adjusting based on current_position
```

## Self-Assessment

1.  Is a manually controlled remote-control car an example of open-loop or closed-loop control? Justify your answer.
2.  What is the main disadvantage of an open-loop control system?
3.  Identify the sensor, actuator, and controller in a simple home heating system with a thermostat.
4.  Why is error calculation a critical step in a closed-loop control system?
5.  Imagine a robot trying to hold a heavy object. Without feedback control, what would likely happen?

---

**Answer Key:**

1.  A manually controlled remote-control car is an example of **closed-loop control**, but the human operator is part of the loop. The human perceives the car's state, compares it to the desired state, and adjusts the controls.
2.  The main disadvantage of an open-loop control system is its inability to compensate for disturbances or changes in the environment, making it inaccurate and unreliable in real-world scenarios.
3.  **Sensor:** Thermometer (measures room temperature). **Actuator:** Heater (turns on/off). **Controller:** Thermostat (compares desired temp to actual temp and sends command to heater).
4.  Error calculation is critical because it quantifies the difference between the desired state and the actual state. This error value is what the controller uses to determine how to adjust the system to achieve its goal.
5.  Without feedback control, the robot would likely not be able to hold the object. Gravity and the object's weight would cause the robot's arm to sag or drop the object, as there would be no mechanism to detect the deviation from the desired position and compensate for it.

## Further Reading

*   [Control Systems 101: Open Loop vs. Closed Loop](https://www.youtube.com/watch?v=R_0_N5_4e0o) - A simple and clear video explanation.
*   [Feedback Control Systems in Robotics](https://robotics.stackexchange.com/questions/336/feedback-control-in-robotics) - A discussion on the topic from a robotics community.
*   *Modern Control Engineering* by Katsuhiko Ogata - A classic (and advanced) textbook on control theory.
