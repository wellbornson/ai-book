--- 
title: "Lesson 7.2: Reinforcement Learning Basics"
sidebar_position: 2
description: "Dive into the exciting world of Reinforcement Learning (RL), where robots learn through trial and error by interacting with their environment to maximize rewards."
tags: [machine-learning, reinforcement-learning, rl, q-learning, policy-gradient]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Define Reinforcement Learning (RL) and its core components (Agent, Environment, State, Action, Reward).
*   Differentiate between policy-based and value-based RL methods.
*   Understand the fundamental concept of a Q-table in Q-learning.
*   Grasp the intuitive idea behind policy gradients.
*   Implement a simple Q-learning algorithm to train a robot to solve a basic navigation task.

## Prerequisites

*   [Lesson 7.1: Supervised Learning for Perception](./lesson-01-supervised-learning-for-perception.md)

## Theory Section

### Learning from Experience: Reinforcement Learning

Unlike supervised learning, where the model is given labeled data, **Reinforcement Learning (RL)** is about learning through interaction and feedback. It's a paradigm of machine learning where an **agent** learns to behave in an **environment** by performing **actions** and observing the **rewards** it receives.

The goal of the agent is to learn a **policy** (a strategy) that maximizes the cumulative reward over time. It's learning through trial and error, much like how a pet is trained with treats.

### The Core Components of Reinforcement Learning

1.  **Agent:** The learner and decision-maker (e.g., the robot, a game character).
2.  **Environment:** The world in which the agent exists and interacts (e.g., the physical room, the game level).
3.  **State (S):** A representation of the environment at a specific point in time (e.g., the robot's position, sensor readings).
4.  **Action (A):** A move the agent can make in the environment (e.g., move forward, turn left, pick up an object).
5.  **Reward (R):** Feedback from the environment that tells the agent how good or bad its last action was. The reward can be positive (a treat) or negative (a penalty).

The agent's life is an endless loop: observe the state, take an action, get a reward, observe the new state, and repeat.

![Reinforcement Learning Loop](https://i.imgur.com/gKkR5aF.png)
*Figure 1: The fundamental agent-environment interaction loop in Reinforcement Learning.*

### Policy vs. Value-Based Methods

There are two main approaches to solving RL problems:

#### 1. Value-Based Methods (e.g., Q-Learning)

*   **Goal:** Learn the "value" of being in a particular state, or the value of taking a particular action in a state. The agent then selects the action that leads to the highest value.
*   **Key Concept: Q-value `Q(s, a)`:** Represents the expected future reward of taking action `a` in state `s`.
*   **How it works:** The agent builds up a table (a **Q-table**) of these values through experience. The policy is implicit: always choose the action with the highest Q-value in the current state.

#### 2. Policy-Based Methods (e.g., Policy Gradients)

*   **Goal:** Directly learn the policy, which is a mapping from states to actions (or probabilities of actions).
*   **Key Concept: Policy `π(a|s)`:** A function that gives the probability of taking action `a` given state `s`.
*   **How it works:** The agent adjusts the parameters of its policy function directly. If an action leads to a high reward, the agent increases the probability of taking that action in that state in the future. Policy gradients are the foundation for many state-of-the-art RL algorithms used in complex robotics tasks.

### Q-Learning: A Simple Value-Based Approach

For environments with a finite number of states and actions, Q-learning is a simple and powerful off-policy RL algorithm.

*   **The Q-Table:** It's a lookup table where rows represent states and columns represent actions. Each cell `Q(s, a)` stores the expected cumulative reward.
*   **The Learning Process (Bellman Equation):** The Q-table is updated using the Bellman equation, which iteratively updates the Q-value based on the immediate reward received and the estimated maximum Q-value of the next state.

    `New_Q(s, a) = (1 - α) * Old_Q(s, a) + α * (Reward + γ * max_Q(s', a'))`

    *   `α` (alpha): The **learning rate**, how much we update our Q-values based on new information.
    *   `γ` (gamma): The **discount factor**, how much we value future rewards. A value closer to 1 means the agent is more farsighted.

*   **Exploration vs. Exploitation:** A key challenge in RL is balancing exploration (trying new, random actions to discover better strategies) and exploitation (using the currently known best strategy to maximize reward). A common strategy is **epsilon-greedy**, where the agent chooses a random action with probability `epsilon` (ε) and the best-known action with probability `1 - epsilon`. Epsilon often starts high and decreases over time as the agent learns more.

### Policy Gradients: Learning the Strategy Directly

For environments with continuous action spaces (e.g., setting a motor torque) or very large state spaces, a Q-table is not feasible. Policy gradient methods address this by directly parameterizing the policy (e.g., with a neural network).

*   **How it works:** The neural network takes a state as input and outputs a probability distribution over actions. The agent samples an action from this distribution, executes it, and observes the reward. It then uses this reward to "nudge" the weights of the network, making good actions more likely and bad actions less likely. This "nudging" is done using gradient ascent on the expected reward.

Policy gradients are the foundation for many state-of-the-art RL algorithms used in complex robotics tasks.

## Practical Section

In this exercise, we will implement a simple Q-learning algorithm to train a "robot" to navigate a 1D "track" to reach a goal. This will demonstrate the core concepts of states, actions, rewards, and the Q-table in a clear, understandable way. We will use a simple text-based simulation.

### The Code

Create a new Python file named `q_learning_track.py`.

The script defines a 1D track environment. The agent can move left or right. The goal is to reach the end of the track. The `QLearningAgent` class encapsulates the Q-table and the learning logic. We then run a training loop for a set number of "episodes."

```python title="q_learning_track.py"
import numpy as np
import time

# --- Environment Setup ---
TRACK_LENGTH = 10
GOAL_STATE = TRACK_LENGTH - 1

class QLearningAgent:
    def __init__(self, num_states, num_actions, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0):
        self.num_states = num_states
        self.num_actions = num_actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        
        # Initialize Q-table with zeros
        self.q_table = np.zeros((num_states, num_actions))
        
    def choose_action(self, state):
        # Exploration vs. Exploitation (epsilon-greedy)
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(self.num_actions) # Explore: choose a random action
        else:
            return np.argmax(self.q_table[state, :]) # Exploit: choose the best known action
            
    def learn(self, state, action, reward, next_state):
        # Q-learning formula (Bellman equation)
        old_value = self.q_table[state, action]
        next_max = np.max(self.q_table[next_state, :])
        
        # Update the Q-value for the state-action pair
        new_value = old_value + self.lr * (reward + self.gamma * next_max - old_value)
        self.q_table[state, action] = new_value

# --- Training Loop ---
if __name__ == "__main__":
    # Agent can move Left (0) or Right (1)
    agent = QLearningAgent(num_states=TRACK_LENGTH, num_actions=2)

    # Training parameters
    num_episodes = 1000
    max_steps_per_episode = 100
    min_epsilon = 0.01
    epsilon_decay_rate = 0.005

    print("--- Starting Q-Learning Training ---")

    for episode in range(num_episodes):
        state = 0 # Start at the beginning of the track
        done = False
        
        for step in range(max_steps_per_episode):
            # 1. Choose an action
            action = agent.choose_action(state)
            
            # 2. Perform the action and get the next state and reward
            if action == 0: # Move Left
                next_state = max(0, state - 1)
            else: # Move Right
                next_state = min(TRACK_LENGTH - 1, state + 1)
            
            # Define rewards
            if next_state == GOAL_STATE:
                reward = 1.0 # High reward for reaching the goal
                done = True
            else:
                reward = -0.1 # Small penalty for each step to encourage efficiency
            
            # 3. Agent learns from the experience
            agent.learn(state, action, reward, next_state)
            
            # Update state
            state = next_state
            
            if done:
                break
        
        # Decay epsilon (exploration rate) over time
        agent.epsilon = max(min_epsilon, agent.epsilon - epsilon_decay_rate)
        
        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}/{num_episodes}, Epsilon: {agent.epsilon:.2f}")

    print("\n--- Training Finished ---")
    print("Final Q-Table:")
    print(agent.q_table.round(2))
    
    # --- Testing the Trained Agent ---
    print("\n--- Testing the Trained Agent (exploitation only) ---")
    agent.epsilon = 0 # No more exploration
    state = 0
    path = [state]
    done = False
    
    while not done:
        action = agent.choose_action(state)
        if action == 0:
            print(f"State: {state}, Action: Move Left")
            state = max(0, state - 1)
        else:
            print(f"State: {state}, Action: Move Right")
            state = min(TRACK_LENGTH - 1, state + 1)
        
        path.append(state)
        
        if state == GOAL_STATE:
            done = True
            
    print(f"\nGoal reached! Path taken: {path}")

```

### Running the Code

Run the script from your terminal: `python q_learning_track.py`.

You will see the output of the training process, with the exploration rate (epsilon) decreasing over time. At the end, the script will print the final **Q-Table**. This table is the "brain" of your trained agent. For each state (row), you can see the learned value for moving Left (column 0) vs. Right (column 1). For states far from the goal, the value for moving Right should be significantly higher.

Finally, the script tests the trained agent, which should now efficiently move from the start to the goal without any random exploration.

## Self-Assessment

1.  What are the five core components of a Reinforcement Learning problem?
2.  What is the main difference between a value-based and a policy-based RL method?
3.  What is the purpose of the "discount factor" (`gamma`) in the Q-learning update rule?
4.  Why is balancing "exploration" and "exploitation" important in RL?
5.  In the `q_learning_track.py` script, why is there a small negative reward for each step?

--- 

**Answer Key:**

1.  The five core components are the **Agent**, **Environment**, **State**, **Action**, and **Reward**.
2.  A **value-based** method learns the value of being in a state or taking an action in a state, and its policy is to choose the highest-value action. A **policy-based** method directly learns the policy (a mapping from states to actions) without necessarily learning a value function.
3.  The discount factor (`gamma`) determines the importance of future rewards. A `gamma` close to 0 makes the agent "myopic" (only caring about immediate rewards), while a `gamma` close to 1 makes the agent "farsighted" (caring about long-term cumulative rewards).
4.  Balancing exploration and exploitation is crucial because the agent needs to **explore** to discover potentially better strategies but also needs to **exploit** its current knowledge to maximize rewards. Too much exploration can lead to suboptimal behavior, while too much exploitation can cause the agent to get stuck with a suboptimal strategy it found early on.
5.  The small negative reward for each step incentivizes the agent to find the *most efficient* path to the goal. Without it, the agent would not care if it takes 5 steps or 500 steps to reach the goal, as long as it gets there eventually.

## Further Reading

*   [Reinforcement Learning, Explained](https://www.youtube.com/watch?v=JgvyzIkgxF0) - A clear and concise video overview.
*   [Introduction to Reinforcement Learning](https://www.deepmind.com/learning-resources/introduction-to-reinforcement-learning-with-david-silver) - The first lecture from David Silver's renowned course.
*   [Q-learning and the Bellman equation](https://www.youtube.com/watch?v=kvo6c0WvL4k) - A more technical but clear explanation.
*   [Policy Gradients Explained](https://www.youtube.com/watch?v=5P7I-xPq8u8) - A simple explanation of the core idea behind policy gradients.
