--- 
title: "Lesson 3.2: Motor Control and PWM"
sidebar_position: 2
description: "Learn how to control motor speed and direction using Pulse Width Modulation (PWM) and H-Bridges, and get a first look at closed-loop PID control."
tags: [actuators, motor-control, pwm, h-bridge, pid]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Explain how Pulse Width Modulation (PWM) is used to control the speed of a DC motor.
*   Understand the function of an H-Bridge motor driver for controlling direction.
*   Describe how encoder feedback enables closed-loop velocity control.
*   Grasp the fundamental concept of PID (Proportional-Integral-Derivative) control.
*   Implement a simulated PWM controller in PyBullet.

## Prerequisites

*   [Lesson 3.1: Actuator Types and Principles](./lesson-01-actuator-types-and-principles.md)

## Theory Section

### The Problem with "Just a Voltage"

In the last lesson, we learned that a DC motor's speed is proportional to the voltage you apply. So, to run a 12V motor at half speed, you could just apply 6V, right?

While technically true, this is inefficient and impractical. A microcontroller (like an Arduino or Raspberry Pi) outputs digital signals (usually 0V or 5V/3.3V) and cannot produce a variable analog voltage directly. Also, trying to reduce a voltage with resistors wastes a lot of energy as heat.

We need a better, digital-friendly way to control motor speed. The solution is **Pulse Width Modulation**.

### Pulse Width Modulation (PWM)

PWM is a clever technique used to control analog circuits with a digital signal. Instead of changing the voltage, we switch the power on and off very quickly, varying the amount of time the power is *on* versus *off*.

*   **Period:** The total time for one on-off cycle. The frequency of a PWM signal is `1 / Period`. This is typically fast enough that the motor doesn't "see" the individual pulses, only the average effect.
*   **Duty Cycle:** The percentage of time within a period that the signal is *on* (high).
    *   A 0% duty cycle means the signal is always off. The motor doesn't move.
    *   A 100% duty cycle means the signal is always on. The motor runs at full speed.
    *   A 50% duty cycle means the signal is on for half the time and off for half the time. The motor runs at roughly half speed.

By precisely controlling the duty cycle, we can achieve fine-grained control over the motor's speed, all while using a simple digital on/off signal.

![PWM Duty Cycles](https://i.imgur.com/u3lM680.png)
*Figure 1: Different PWM duty cycles. The motor responds to the "average" voltage, effectively controlling its speed.*

### Changing Direction: The H-Bridge

PWM is great for speed, but how do we reverse a DC motor's direction? We need to be able to reverse the polarity of the voltage applied to it. The standard circuit for this is called an **H-Bridge**.

An H-Bridge is a circuit containing four switches (usually transistors). By closing these switches in pairs, we can change the direction that current flows through the motor.

*   To spin forward, close switches 1 and 4.
*   To spin backward, close switches 2 and 3.

Closing switches 1 and 2 (or 3 and 4) at the same time would create a short circuit, so motor driver chips have built-in logic to prevent this. This is sometimes called a "shoot-through" condition.

![H-Bridge Circuit](https://i.imgur.com/m4h8C6i.png)
*Figure 2: An H-Bridge circuit. By changing which switches are closed, we can control the direction of current through the motor (M).*

A **motor driver** is a chip or module that combines an H-Bridge with other protection and control circuitry. It allows a low-power microcontroller signal to control a high-power motor safely.

### Closing the Loop: PID Control

PWM and an H-Bridge give us open-loop control. We can set a duty cycle that *should* correspond to a certain speed, but what if the robot starts going up a hill? The motor will slow down, even though our command hasn't changed.

To maintain a desired speed under changing loads, we need **closed-loop control**. This means using a sensor (like an encoder) to measure the motor's actual speed and continuously adjust the PWM signal to correct for any error.

The most common algorithm for this is **PID (Proportional-Integral-Derivative) control**.

A PID controller calculates an output command based on three terms:

1.  **The Proportional (P) Term:** This term is proportional to the **current error**.
    *   `Error = Target Speed - Actual Speed`
    *   If you are far from your target, the P term provides a large corrective force. If you are close, it provides a small one.
    *   *Problem:* Using only P control often leads to a **steady-state error** (never quite reaching the target) or **overshoot** (shooting past the target).

2.  **The Integral (I) Term:** This term looks at the **sum of past errors**.
    *   If you have a small, persistent steady-state error, the I term will gradually increase over time, adding more and more force until the error is eliminated.
    *   *Problem:* The I term can cause significant overshoot if not tuned carefully.

3.  **The Derivative (D) Term:** This term looks at the **rate of change of the error**.
    *   It acts as a brake or damper. As you get closer to the target, the error is decreasing. The D term resists this change, slowing the motor down to prevent it from overshooting the target.
    *   *Problem:* The D term is very sensitive to sensor noise.

**Output = (P * current_error) + (I * sum_of_past_errors) + (D * rate_of_error_change)**

By "tuning" the three constants (Kp, Ki, Kd), an engineer can design a controller that is fast, stable, and accurate. We will dive much deeper into PID in Chapter 5.

## Practical Section

For this exercise, we will simulate PWM control in PyBullet. While PyBullet doesn't have a built-in PWM function, we can mimic it. The `p.setJointMotorControl2` function with `VELOCITY_CONTROL` is actually a high-level command that has its own internal PID controller.

To better simulate the effect of PWM, we will use `TORQUE_CONTROL`. This allows us to directly command the force (or torque) applied to a joint, which is the physical result of the electrical power controlled by PWM. A higher duty cycle results in a higher average torque.

### The Code

Create a new file named `pwm_simulation.py` and copy the code below.

The script loads a simple pendulum-like object (a long box on a hinge). We will then write a loop that simulates a PWM signal by applying a torque for a certain portion of each "period".

```python title="pwm_simulation.py"
import pybullet as p
import time

# --- Setup ---
p.connect(p.GUI)
p.setGravity(0,0,-10)

# Create a simple pendulum
base = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.1])
link = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.5])

base_id = p.createMultiBody(baseCollisionShapeIndex=base, basePosition=[0, 0, 1])
link_id = p.createMultiBody(linkCollisionShapeIndex=link, basePosition=[0, 0, 1.6])

# Create a revolute joint (hinge) to connect them
joint_id = p.createConstraint(
    parentBodyUniqueId=base_id,
    parentLinkIndex=-1,
    childBodyUniqueId=link_id,
    childLinkIndex=-1,
    jointType=p.JOINT_REVOLUTE,
    jointAxis=[0, 1, 0], # Hinge around the Y-axis
    parentFramePosition=[0, 0, 0.1],
    childFramePosition=[0, 0, -0.5]
)

# --- PWM Simulation Loop ---
# We will simulate a period of 100 simulation steps
period = 100
step_counter = 0

# Let's try different duty cycles
duty_cycles = [0.25, 0.5, 0.75, 1.0] # 25%, 50%, 75%, 100%
max_torque = 5.0 # The torque to apply when the "pulse" is on

print("Starting PWM demonstration. Each duty cycle will run for 5 seconds.")

for dc in duty_cycles:
    print(f"\nTesting Duty Cycle: {dc*100}%")
    on_duration = int(period * dc) # How long the pulse is 'on'

    for i in range(240 * 5): # Run for 5 seconds
        step_counter = (step_counter + 1) % period

        torque = 0
        if step_counter < on_duration:
            # The pulse is ON, apply torque
            torque = max_torque
        # else the pulse is OFF, torque remains 0

        p.setJointMotorControl2(
            bodyIndex=link_id,
            jointIndex=-1, # Control the base of the multibody
            controlMode=p.TORQUE_CONTROL,
            force=torque
        )

        p.stepSimulation()
        time.sleep(1./240.)

print("\nDemonstration finished.")
p.disconnect()
```

### Running the Code

Run the script from your terminal: `python pwm_simulation.py`.

You will see a pendulum swing. Observe its behavior carefully. It will run for 20 seconds total.
*   For the first 5 seconds (25% duty cycle), it will swing slowly.
*   For the next 5 seconds (50% duty cycle), it will swing noticeably faster and higher.
*   This continues until the last 5 seconds (100% duty cycle), where the torque is always on, causing it to spin rapidly.

This demonstrates the core principle of PWM: by changing the *width* of the "on" pulse, we effectively control the average power delivered to the motor.

## Self-Assessment

1.  What is the "duty cycle" of a PWM signal?
2.  What is the primary function of an H-Bridge circuit?
3.  Why is closed-loop control generally preferable to open-loop control for maintaining a constant speed?
4.  What does the "P" in PID control stand for, and what is its main job?
5.  If you want to run a 12V DC motor at 25% of its maximum speed using PWM, what would the duty cycle be?

---

**Answer Key:**

1.  The duty cycle is the percentage of time within one full period that the signal is active or "on" (high).
2.  An H-Bridge allows you to reverse the direction of the current flowing through a motor, thus reversing its direction of rotation.
3.  Closed-loop control uses sensor feedback to actively compensate for external disturbances (like hills or changing loads), whereas open-loop control cannot.
4.  "P" stands for **Proportional**. Its job is to apply a corrective force that is directly proportional to the current error between the target state and the actual state.
5.  The duty cycle would be 25%.

## Further Reading

*   [PWM Tutorial by SparkFun](https://learn.sparkfun.com/tutorials/pulse-width-modulation/all)
*   [How H-Bridges Work](https://www.youtube.com/watch?v=m4h8C6i.png) - A great video explanation.
*   [Understanding PID Control, Part 1: What is PID Control?](https://www.matlab.com/videos/understanding-pid-control-part-1-what-is-pid-control-1490282424933.html) - An intuitive video from MATLAB.
