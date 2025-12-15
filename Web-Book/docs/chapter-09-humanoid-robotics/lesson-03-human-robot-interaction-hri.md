--- 
title: "Lesson 9.3: Human-Robot Interaction (HRI)"
sidebar_position: 3
description: "Explore the fascinating field of Human-Robot Interaction (HRI), learning how robots use social cues like gaze and gesture to interact safely and intuitively with people."
tags: [humanoid-robotics, hri, social-robotics, ethics, interaction-design]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Define Human-Robot Interaction (HRI) as a field of study.
*   Identify key communication channels for social robots (gaze, gesture, speech).
*   Understand the importance of safety and predictability in physical HRI.
*   Discuss the principles of designing intuitive and effective robot interactions.
*   Consider the ethical implications of deploying social robots in society.

## Prerequisites

*   [Lesson 9.1: Humanoid Robot Design and Kinematics](./lesson-01-humanoid-robot-design-and-kinematics.md)
*   [Lesson 1.2: Safety and Ethics in Robotics](../chapter-01-introduction/lesson-02-safety-and-ethics.md)

## Theory Section

### Beyond the Physical: The Social Robot

Up to this point, we have focused on the physical aspects of robotics: how robots move, see, and manipulate objects. But for humanoid robots, which are designed to operate in human environments, there is another critical dimension: **social interaction**.

**Human-Robot Interaction (HRI)** is a multidisciplinary field dedicated to understanding, designing, and evaluating robotic systems for use by or with humans. It combines robotics, artificial intelligence, social psychology, design, and ethics. The goal is to create robots that are not just functional, but also safe, intuitive, and effective partners for people.

### Communication Channels in HRI

Humans use a rich set of verbal and non-verbal cues to communicate. For a robot to be an effective social partner, it must be able to both understand and generate these cues.

#### 1. Gaze and Head Pose
Where a robot is "looking" is a powerful signal.
*   **Expressing Intent:** A robot can signal its intention by looking at an object before it moves to pick it up. This makes its actions predictable and less startling to humans.
*   **Turn-Taking in Conversation:** In a conversation, a robot can use its gaze to indicate whose turn it is to speak.
*   **Gathering Information:** The robot's "head" (with its cameras and sensors) must be directed towards the person or object it is interacting with.

#### 2. Gesture and Body Language
A humanoid's arms and body can be used for more than just manipulation.
*   **Deictic Gestures:** Pointing to an object or location ("please pick up *that* book").
*   **Iconic Gestures:** Using hands to show the size or shape of an object.
*   **Body Posture:** A robot's posture can convey its state. For example, a robot might slump slightly to indicate it is in a low-power or idle mode.

#### 3. Speech and Language
*   **Speech Recognition:** The ability to understand spoken commands and questions from a human.
*   **Natural Language Processing (NLP):** Understanding the *meaning* and *intent* behind the words.
*   **Speech Synthesis:** Generating clear, natural-sounding speech to communicate information, ask questions, or provide feedback.

### Designing for Intuitive Interaction

A core principle of HRI is that humans should not have to be robotics experts to interact with a robot. The interaction should be **intuitive and predictable**.

*   **Legibility:** The robot's actions should be easy for a person to understand. Its movements and intentions should be clear and unambiguous.
*   **Predictability:** The robot should behave in ways that a person would expect, following social norms and logical task sequences.
*   **Feedback:** The robot should provide clear feedback to the user about its state and understanding. This can be through lights, sounds, speech, or on-screen displays. For example, if a robot hears a command, it might nod or say "Okay" to confirm it understood.

### Safety in Physical HRI

When a powerful robot and a human share the same physical space, safety is paramount. This goes beyond the E-stops we've discussed and enters the realm of **collaborative robotics**.

*   **Collision Avoidance:** The robot must actively track humans in its workspace and plan paths that avoid them.
*   **Compliant Control:** Using impedance or admittance control (as discussed in Lesson 8.1) allows the robot to be "soft" and yield to unexpected contact, rather than rigidly pushing against it.
*   **Speed and Force Limiting:** In collaborative modes, a robot's speed and force are often limited to levels that are safe for human contact.

### Ethical Considerations for Social Robots

As social robots become more integrated into our lives – in healthcare, education, and elder care – we must confront significant ethical questions.

*   **Deception and Anthropomorphism:** Should a robot be designed to appear as if it has emotions or consciousness? Is it deceptive to create a "robot friend" for an elderly person that doesn't genuinely "care"?
*   **Privacy:** Social robots in the home are equipped with cameras and microphones, collecting vast amounts of sensitive data. Who owns this data? How is it used and protected?
*   **Attachment and Dependency:** Can vulnerable people (especially children or the elderly) form unhealthy attachments to social robots? What happens if the robot is taken away or breaks?
*   **Bias:** If a robot's interaction logic is trained on data from one culture, will it behave appropriately and fairly when interacting with people from another culture?

There are no easy answers to these questions, and they are the subject of ongoing research and public debate. As robot designers, we have a responsibility to consider these impacts.

## Practical Section

Implementing a full HRI system with speech and gesture recognition is a major undertaking. For this exercise, we'll create a simplified simulation of a robot exhibiting a fundamental HRI behavior: **gaze following**.

We will load a robot model with a head. We will then create a "human" representation (a simple sphere) that can be moved around with sliders. The robot's task will be to continuously track the "human" with its head, always keeping it in the center of its view.

### The Code

Create a new Python file named `hri_gaze.py`.

The script loads a KUKA robot (which has a head-like final link). It then creates a red sphere to represent a person's head and sliders to move this sphere. In the main loop, the robot calculates the direction to the red sphere and uses Inverse Kinematics to solve for the joint angles needed to make its "head" (the end-effector) "look at" the sphere.

```python title="hri_gaze.py"
import pybullet as p
import time
import pybullet_data
import numpy as np

# --- Setup ---
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -10)
p.setRealTimeSimulation(0)

p.loadURDF("plane.urdf")
# Load a robot. We'll use the KUKA arm and treat its end-effector as the "head".
robot_id = p.loadURDF("kuka_lbr_iiwa/model.urdf", basePosition=[0,0,0], useFixedBase=True)
num_joints = p.getNumJoints(robot_id)
head_link_index = 6 # The end-effector link

# --- "Human" Simulation ---
# Create a sphere to represent a person's head
human_shape = p.createVisualShape(p.GEOM_SPHERE, radius=0.1, rgbaColor=[1,0,0,1])
human_id = p.createMultiBody(baseVisualShapeIndex=human_shape, basePosition=[1, 0, 1])

# Create sliders to move the "human"
human_x_slider = p.addUserDebugParameter("Human X", -2, 2, 1)
human_y_slider = p.addUserDebugParameter("Human Y", -2, 2, 0)
human_z_slider = p.addUserDebugParameter("Human Z", 0, 2, 1)

# --- Gaze Following Controller ---
print("--- Starting HRI Gaze Following Simulation ---")
print("Move the sliders to move the 'human' (red sphere).")
print("The robot will try to keep the sphere in its 'gaze'.")

try:
    while True:
        # 1. Get the position of the "human" from the sliders
        human_pos = [
            p.readUserDebugParameter(human_x_slider),
            p.readUserDebugParameter(human_y_slider),
            p.readUserDebugParameter(human_z_slider)
        ]
        p.resetBasePositionAndOrientation(human_id, human_pos, [0,0,0,1])
        
        # 2. Get the current position of the robot's "head"
        head_state = p.getLinkState(robot_id, head_link_index)
        head_pos = head_state[0]
        
        # 3. Calculate the desired orientation for the robot's head
        # We want the head's Z-axis (in its local frame) to point at the human
        # By convention, the local Z-axis of a link often points "out".
        # We will calculate a quaternion that achieves this.
        # This is a common IK problem: solve for orientation.
        
        # First, we need a position target for the IK solver. We'll keep the head
        # in a fixed location and only solve for orientation.
        ik_target_pos = [0.5, 0, 1.2] 
        
        # We want the head to "look at" the human. Let's define the "look" vector
        # in the head's local coordinate system. Let's say it's the head's local X-axis.
        # So we want the head's X-axis to point towards the human.
        # We can construct a rotation matrix and then convert to a quaternion.
        # A simpler way with PyBullet is to use a constraint-based IK or a trick.
        # For simplicity here, we'll use a less direct method:
        # We'll calculate an orientation quaternion that makes the robot look at the target.
        # A full implementation would involve creating a rotation matrix.
        
        # A simpler IK formulation for "look at" is to constrain the position
        # and just provide an orientation. Here, we calculate a target orientation.
        # This is a complex topic, so we'll use a simplified target orientation for demonstration.
        # We can use p.getQuaternionFromEuler to create a target orientation,
        # but calculating the correct Euler angles to look at a point is non-trivial.
        # The most robust way is to use calculateInverseKinematics with a target orientation.
        # For this demo, let's just point the end effector towards the human.
        
        # Let's use a simpler approach: solve IK to make the head point at the human.
        # The 'targetOrientation' for `calculateInverseKinematics` is what we need.
        # A full derivation is complex. Instead, let's just move the whole arm
        # in a way that "looks" at the target.
        
        # Let's stick with the KUKA and just control the first and fourth joints.
        # Joint 0: Base rotation (Yaw)
        # Joint 3: Elbow/arm tilt (Pitch) 
        
        # Calculate yaw angle to face the human
        dx = human_pos[0] - robot_id.getBasePositionAndOrientation(robot_id)[0][0]
        dy = human_pos[1] - robot_id.getBasePositionAndOrientation(robot_id)[0][1]
        target_yaw = np.arctan2(dy, dx)
        
        # Calculate pitch angle
        dist = np.sqrt(dx**2 + dy**2)
        dz = human_pos[2] - head_pos[2]
        target_pitch = np.arctan2(dz, dist)

        # Let's set the joints directly
        p.setJointMotorControl2(robot_id, 0, p.POSITION_CONTROL, targetPosition=target_yaw, force=500)
        # We'll use joint 3 for pitch-like motion
        p.setJointMotorControl2(robot_id, 3, p.POSITION_CONTROL, targetPosition=-target_pitch, force=500)

        # Keep other joints somewhat neutral
        for i in [1,2,4,5,6]:
            p.setJointMotorControl2(robot_id, i, p.POSITION_CONTROL, targetPosition=0, force=100)

        p.stepSimulation()
        time.sleep(1./240.)

except KeyboardInterrupt:
    print("Simulation interrupted.")
finally:
    print("\nHRI Gaze Simulation Finished.")
    p.disconnect()
```

### Running the Code

Run the script from your terminal: `python hri_gaze.py`.

A KUKA arm will appear, along with a red sphere and three sliders. Move the sliders to change the position of the red sphere. You will see the robot's base (joint 0) rotate and its arm (joint 3) tilt up and down, trying to keep its end-effector "looking" at the sphere.

This simple reactive behavior is a fundamental building block of HRI. It makes the robot appear more aware and intentional, which is crucial for intuitive human-robot collaboration.

## Self-Assessment

1.  What is the primary goal of the field of Human-Robot Interaction (HRI)?
2.  Name two non-verbal cues a humanoid robot can use to communicate its intent.
3.  Why is "predictability" an important principle in HRI design?
4.  What is a major ethical concern related to social robots in elder care?
5.  In our `hri_gaze.py` simulation, what does the robot do to "look at" the target sphere?

--- 

**Answer Key:**

1.  The primary goal of HRI is to design, understand, and evaluate robotic systems that are safe, intuitive, and effective for use by or with humans.
2.  Non-verbal cues include **gaze** (where the robot is looking), **gestures** (e.g., pointing), and **body posture**.
3.  Predictability is important because it makes the robot's actions understandable and less startling to humans. If a person can anticipate what the robot will do next, they will feel safer and more comfortable working alongside it.
4.  A major ethical concern is the potential for **deception and emotional attachment**. An elderly person might form a one-sided emotional bond with a robot that is only simulating companionship, which could have negative psychological effects. Privacy is another major concern.
5.  The robot uses a simplified control strategy: it rotates its base to **face** the sphere (controlling its yaw) and tilts one of its arm joints up or down to adjust its **pitch**, keeping the sphere in its general forward direction.

## Further Reading

*   [The Rise of Social Robots](https://www.youtube.com/watch?v=kYJru4A3t5o) - A TED talk by Heather Knight on social robotics.
*   *The Media Equation* by Byron Reeves and Clifford Nass - A foundational book on how people treat computers, television, and new media like real people and places.
*   [The HRI Conference](https://humanrobotinteraction.org/) - The website for the premier academic conference on HRI, showcasing the latest research.
*   *Robot Ethics 2.0: From Autonomous Cars to Artificial Intelligence* - A book exploring the ethical challenges of advanced robotics.
