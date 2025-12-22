--- 
title: "Lesson 10.2: Multi-Robot Systems and Coordination"
sidebar_position: 2
description: "Venture into the world of multi-robot systems, exploring the challenges of communication and coordination, swarm intelligence, and collaborative tasks like formation control."
tags: [multi-robot, swarm-robotics, coordination, distributed-control, formation-control]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Identify the key challenges in multi-robot systems (communication, coordination, task allocation).
*   Differentiate between centralized and decentralized control architectures.
*   Understand the basic principles of swarm robotics and emergent behavior.
*   Describe common multi-robot tasks like formation control and cooperative manipulation.
*   Implement a simple formation control simulation with multiple robots in PyBullet.

## Prerequisites

*   [Lesson 10.1: System Integration and Architecture](./lesson-01-system-integration-and-architecture.md)
*   [Lesson 6.2: Obstacle Avoidance and Reactive Navigation](../chapter-06-motion-planning/lesson-02-obstacle-avoidance-and-reactive-navigation.md)

## Theory Section

### More Robots, More Problems?

Why use multiple robots instead of one, more capable robot? A team of robots can offer significant advantages:
*   **Parallelism:** Multiple tasks can be accomplished at the same time.
*   **Robustness:** The system can continue to function even if some robots fail.
*   **Scalability:** The system's capabilities can be expanded by simply adding more robots.
*   **Spatial Distribution:** Tasks that are spread out over a large area (like environmental monitoring or search and rescue) are better handled by a team.

However, moving from a single robot to a **Multi-Robot System (MRS)** introduces a new set of complex challenges.

### Key Challenges in Multi-Robot Systems

1.  **Communication:** How do robots share information?
    *   **Bandwidth:** Wireless channels have limited capacity.
    *   **Range:** Robots may move out of communication range.
    *   **Reliability:** Communication can be noisy or lost.

2.  **Coordination:** How do robots synchronize their actions to achieve a common goal? This includes avoiding collisions with each other, sequencing tasks, and moving in a coherent manner.

3.  **Task Allocation:** Who does what? How does the team decide which robot should perform which task, especially when tasks are dynamic and robots have different capabilities?

4.  **Localization and Mapping:** In addition to localizing itself, each robot must also be aware of the positions of its teammates.

### Centralized vs. Decentralized Control

The architecture of an MRS can be broadly categorized in two ways:

*   **Centralized Control:**
    *   **How it works:** A single central computer (the "base station") makes all the decisions for the entire team. It gathers sensor data from all robots, computes a global plan, and sends specific commands to each robot.
    *   **Advantages:** Optimal solutions are easier to find since the central planner has a complete world view.
    *   **Disadvantages:** Creates a single point of failure (if the central computer goes down, the whole system stops). Requires high communication bandwidth. Does not scale well to very large teams.

*   **Decentralized (or Distributed) Control:**
    *   **How it works:** Each robot makes its own decisions based on its local sensor data and information received from its immediate neighbors. There is no central commander.
    *   **Advantages:** Highly robust and scalable. The failure of one robot does not bring down the system. Low communication overhead.
    *   **Disadvantages:** Achieving optimal, globally coherent behavior is much more difficult. Decisions are based on incomplete information.

### Swarm Robotics and Emergent Behavior

**Swarm robotics** is a specific area of decentralized control inspired by social insects like ants, bees, and termites. It focuses on using a large number of simple, often identical robots that follow a set of simple rules.

The key concept is **emergent behavior**. Complex, global-level intelligence (like building a nest or finding the shortest path to food) "emerges" from the local interactions of many simple agents, even though no single agent has a concept of the global plan.

**Example: Ant-like Foraging**
1.  **Rule 1:** Move randomly.
2.  **Rule 2:** If you find "food," pick it up and return to the "nest," leaving a "pheromone" trail.
3.  **Rule 3:** If you sense a pheromone trail, follow it.

This simple set of local rules leads to the emergent global behavior of the entire swarm efficiently finding and retrieving all the food.

### Common Multi-Robot Tasks

*   **Formation Control:** Making a group of robots move while maintaining a specific geometric shape (e.g., a line, a V-shape, a circle). This is crucial for applications like aerial surveillance, cooperative transport, and mobile sensor networks.
*   **Cooperative Manipulation:** Using multiple robot arms to lift or manipulate a single, large object that would be too heavy or unwieldy for one robot. This requires precise coordination of forces and movements.
*   **Area Coverage:** Systematically exploring and mapping an unknown area with a team of robots, ensuring the entire area is covered efficiently.
*   **Task Allocation (Market-Based):** A common decentralized approach where robots "bid" on tasks. The robot that can perform the task most efficiently (e.g., is closest, has the right tools) "wins" the bid and executes the task.

## Practical Section

In this exercise, we will implement a simple **decentralized formation control** algorithm. We will spawn three robots and program them to maintain a triangular formation while moving towards a goal. Each robot will only have knowledge of its own position, the goal's position, and the positions of its immediate neighbors.

### The Code

Create a new Python file named `formation_control.py`.

The script will load three `racecar` models. The main loop will iterate through each robot, and for each one, it will:
1.  Calculate an "attractive" force towards its designated spot in the formation.
2.  Calculate "repulsive" forces from the other robots to avoid collisions.
3.  Sum these forces to determine its movement commands, similar to the potential fields method from Lesson 6.2.

``` title="formation_control.py"
import pybullet as p
import time
import pybullet_data
import numpy as np

# --- Parameters ---
NUM_ROBOTS = 3
FORMATION_GOAL = np.array([5.0, 0.0]) # The target for the center of the formation

# --- Robot Controller Class ---
class FormationRobot:
    def __init__(self, robot_id, formation_offset):
        self.robot_id = robot_id
        self.formation_offset = formation_offset # My desired position relative to the formation center
        self.wheel_indices = [5, 7]
        self.wheel_radius = 0.1
        self.wheel_base = 0.5
        self.max_vel = 10.0

    def set_velocities(self, v_linear, omega_angular):
        v_left = v_linear - (omega_angular * self.wheel_base / 2)
        v_right = v_linear + (omega_angular * self.wheel_base / 2)
        target_left = np.clip(v_left / self.wheel_radius, -self.max_vel, self.max_vel)
        target_right = np.clip(v_right / self.wheel_radius, -self.max_vel, self.max_vel)
        p.setJointMotorControl2(self.robot_id, self.wheel_indices[0], p.VELOCITY_CONTROL, targetVelocity=target_left, force=100)
        p.setJointMotorControl2(self.robot_id, self.wheel_indices[1], p.VELOCITY_CONTROL, targetVelocity=target_right, force=100)
        
    def update(self, other_robot_positions, formation_center):
        # --- Decentralized Control Logic for one robot ---
        current_pos_xyz, current_ori_q = p.getBasePositionAndOrientation(self.robot_id)
        current_pos = np.array(current_pos_xyz[:2])
        current_yaw = p.getEulerFromQuaternion(current_ori_q)[2]
        
        # 1. Attractive force towards my spot in the formation
        my_target_spot = formation_center + self.formation_offset
        attractive_force = 0.5 * (my_target_spot - current_pos)
        
        # 2. Repulsive force from other robots
        repulsive_force = np.array([0.0, 0.0])
        for other_pos in other_robot_positions:
            if np.array_equal(other_pos, current_pos): continue # Don't repel myself
            
            vec_from_other = current_pos - other_pos
            dist = np.linalg.norm(vec_from_other)
            
            if dist < 1.5 and dist > 0: # Repel if closer than 1.5 meters
                repulsive_force += 0.3 * (1/dist - 1/1.5) * (vec_from_other / dist)
                
        # 3. Sum forces
        resultant_force = attractive_force + repulsive_force
        
        # 4. Convert force to velocity commands
        desired_heading = np.arctan2(resultant_force[1], resultant_force[0])
        angular_error = desired_heading - current_yaw
        angular_error = np.arctan2(np.sin(angular_error), np.cos(angular_error))
        
        v_linear = np.clip(np.linalg.norm(resultant_force), 0, 0.8)
        omega_angular = np.clip(angular_error * 2.0, -np.pi/2, np.pi/2)
        
        self.set_velocities(v_linear, omega_angular)

# --- Main Simulation ---
if __name__ == "__main__":
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -10)
    
    p.loadURDF("plane.urdf")
    
    # Define formation offsets (a triangle)
    offsets = [
        np.array([0, 1.0]),  # Robot 1 (Top)
        np.array([-1.0, -0.5]), # Robot 2 (Bottom-left)
        np.array([1.0, -0.5])   # Robot 3 (Bottom-right)
    ]
    
    # Create the robots
    robots = []
    start_positions = [[0,1,0.1], [-1,-0.5,0.1], [1,-0.5,0.1]]
    for i in range(NUM_ROBOTS):
        robot_id = p.loadURDF("racecar/racecar.urdf", basePosition=start_positions[i])
        robots.append(FormationRobot(robot_id, offsets[i]))
        
    print("--- Starting Multi-Robot Formation Control Simulation ---")
    
    current_formation_center = np.array([0.0, 0.0]) # The center of the formation starts at the origin
    
    try:
        while np.linalg.norm(current_formation_center - FORMATION_GOAL) > 0.5:
            # --- Centralized part (for this simple demo): Update the formation's goal ---
            # In a real system, this could be a broadcasted waypoint
            # Move the formation center towards the final goal
            direction_to_goal = FORMATION_GOAL - current_formation_center
            if np.linalg.norm(direction_to_goal) > 0:
                current_formation_center += (direction_to_goal / np.linalg.norm(direction_to_goal)) * 0.01

            # Get all current robot positions (for calculating repulsion)
            all_robot_positions = []
            for robot in robots:
                pos, _ = p.getBasePositionAndOrientation(robot.robot_id)
                all_robot_positions.append(np.array(pos[:2]))
                
            # --- Decentralized part: Update each robot ---
            for robot in robots:
                robot.update(all_robot_positions, current_formation_center)

            p.stepSimulation()
            time.sleep(1./240.)
            
    except KeyboardInterrupt:
        print("Simulation interrupted.")
    finally:
        for robot in robots: # Stop all robots
            robot.set_velocities(0,0)
        print("\nSimulation Finished.")
        time.sleep(2)
        p.disconnect()
```

### Running the Code

Run the script from your terminal: `python formation_control.py`.

You will see three racecar robots. They will arrange themselves into a triangle formation and then begin moving together across the simulation towards the goal at `(5, 0)`. Each robot independently calculates its required movement based on its desired spot in the formation and repulsion from its neighbors. This demonstrates a simple, decentralized multi-robot control system.

## Self-Assessment

1.  What is a major disadvantage of a centralized control architecture for a large team of robots?
2.  What is "emergent behavior" in the context of swarm robotics?
3.  What is the main goal of "formation control"?
4.  In our `formation_control.py` script, what are the two main "forces" that dictate each robot's movement?
5.  Is the control logic within each `FormationRobot.update()` method centralized or decentralized? Why?

---

**Answer Key:**

1.  A major disadvantage is that it has a **single point of failure**. If the central controller fails, the entire system stops. It also does not scale well to a large number of robots due to communication bottlenecks.
2.  Emergent behavior is when complex, global-level patterns or intelligence arise from the local interactions of many simple agents, even though no single agent has knowledge of the global plan.
3.  The main goal of formation control is to make a group of robots move while maintaining a specific, predefined geometric shape.
4.  The two main forces are an **attractive force** pulling the robot towards its designated spot in the formation, and a **repulsive force** pushing it away from its neighbors to avoid collision.
5.  The control logic within each `update()` method is **decentralized**. Each robot makes its own decision based on its own target and the positions of its neighbors, without a central controller telling it exactly where to go or how fast to move.

## Further Reading

*   [Swarm Robotics: A Brief Introduction](https://www.youtube.com/watch?v=kYJru4A3t5o) - A high-level overview.
*   [Multi-Robot Systems](https://www.cs.cmu.edu/~motionplanning/lecture/Chap13-MRS_howie.pdf) - A university lecture on the topic.
*   [Kilobots: A Low-Cost Scalable Robot System for Collective Behaviors](https://www.youtube.com/watch?v=s-68k9aHQ60) - A video showcasing a real swarm robotics platform.
*   [Cooperative Object Transport with Multiple Robots](https://www.youtube.com/watch?v=dQw4w9WgXcQ) - A video demonstrating cooperative manipulation. (Note: Placeholder link, but search for this title for relevant research videos).

```