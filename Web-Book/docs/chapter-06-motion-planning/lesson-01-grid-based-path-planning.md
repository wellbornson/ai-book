--- 
title: "Lesson 6.1: Grid-Based Path Planning"
sidebar_position: 1
description: "Discover how robots find optimal paths through known environments using grid maps and classic algorithms like Dijkstra's and A*."
tags: [path-planning, navigation, a-star, dijkstra, occupancy-grid]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Define the path planning problem in robotics.
*   Understand and create a simple occupancy grid representation of an environment.
*   Explain the principles of Dijkstra's algorithm for finding shortest paths.
*   Describe how the A* algorithm improves upon Dijkstra's by using heuristics.
*   Implement the A* algorithm to find a path in a 2D grid in Python.

## Prerequisites

*   [Lesson 4.3: Mobile Robot Kinematics](../chapter-04-kinematics-and-dynamics/lesson-03-mobile-robot-kinematics.md) (Understanding of robot motion)

## Theory Section

### The Robot's GPS: Finding a Way

Imagine you want a robot to move from one side of a room to another, avoiding furniture. How does it figure out *how* to get there? This is the core problem of **path planning**, sometimes called **motion planning**.

The goal of path planning is to find a sequence of valid configurations (a path) that takes a robot from a starting configuration to a target configuration, typically while avoiding obstacles and optimizing some criterion (e.g., shortest distance, fastest time, minimum energy).

In this lesson, we'll focus on **grid-based path planning**, which is suitable for robots operating in known, static, and discretized environments.

### Occupancy Grids: The Robot's Map

For grid-based planning, the robot's environment is represented as an **occupancy grid**.
*   The environment is divided into a grid of cells (or "pixels").
*   Each cell is marked as either **free** (navigable) or **occupied** (contains an obstacle).
*   Sometimes, cells can also be marked as **unknown** or have a probability of occupancy.

An occupancy grid is a simple yet powerful way to represent complex environments for navigation.

![Occupancy Grid](https://i.imgur.com/uNf4lVj.png)
*Figure 1: A simple 2D occupancy grid where black cells are obstacles and white cells are free space. The robot needs to find a path from Start (S) to Goal (G).*

### Dijkstra's Algorithm: Shortest Path for All

**Dijkstra's algorithm** is a classic graph search algorithm that finds the shortest paths from a single source node to all other nodes in a graph with non-negative edge weights. In our grid, each cell is a node, and moving from one cell to an adjacent cell is an edge with a weight (cost).

*   **How it works:**
    1.  Starts at the source node and assigns a distance of 0 to it and infinity to all other nodes.
    2.  It iteratively visits unvisited nodes, calculates the distance to its neighbors, and updates their distances if a shorter path is found.
    3.  It always chooses to visit the unvisited node with the smallest known distance.
*   **Strengths:** Guarantees to find the shortest path.
*   **Weaknesses:** Explores in all directions, which can be computationally expensive for large grids, as it expands many nodes that are not on the optimal path to the goal.

### A* (A-Star) Algorithm: Dijkstra with a Guide

**A* (pronounced "A-star") algorithm** is one of the most widely used pathfinding algorithms. It's essentially Dijkstra's algorithm, but it's made much more efficient by using a **heuristic** function.

*   **Heuristic (h(n)):** An estimated cost from the current node `n` to the goal node. For grid-based movement, common heuristics include:
    *   **Manhattan Distance:** `abs(x1 - x2) + abs(y1 - y2)` (for movement restricted to up/down/left/right).
    *   **Euclidean Distance:** `sqrt((x1 - x2)^2 + (y1 - y2)^2)` (for movement in any direction).
*   **Cost Function (f(n)):** A* minimizes `f(n) = g(n) + h(n)`.
    *   `g(n)`: The actual cost from the start node to node `n`.
    *   `h(n)`: The estimated cost from node `n` to the goal.

*   **How it works:** Like Dijkstra's, A* explores nodes, but it prioritizes nodes that are likely to be on the shortest path to the goal because of the heuristic. It always explores the node with the lowest `f(n)`.
*   **Strengths:** Optimal (finds the shortest path) and much more efficient than Dijkstra's for many problems because the heuristic guides the search towards the goal.
*   **Weaknesses:** Still computationally intensive for very large or complex environments. The quality of the heuristic affects performance significantly.

#### Admissibility and Consistency of Heuristics

For A* to guarantee finding the optimal path:
*   **Admissibility:** The heuristic `h(n)` must *never overestimate* the actual cost to reach the goal. (e.g., Euclidean distance is admissible).
*   **Consistency:** A slightly stronger condition, related to how `h(n)` changes between adjacent nodes.

## Practical Section

In this exercise, we will implement the A* algorithm in Python to find the shortest path on a 2D occupancy grid. We won't use PyBullet for this directly, as pathfinding is a more abstract algorithmic problem. Instead, we'll represent our grid as a 2D array and visualize the path using text.

### The Code

Create a new Python file named `a_star_pathfinding.py`.

This script defines a `Node` class to hold information about each cell in our grid (position, `g_cost`, `h_cost`, parent). The A* algorithm is implemented using a priority queue (Python's `heapq` module) to efficiently select the next node to explore.

```python title="a_star_pathfinding.py"
import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost from current node to end node
        self.f = 0  # Total cost (g + h)

    # For priority queue comparison
    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

def heuristic(node_pos, goal_pos):
    """
    Manhattan distance heuristic for grid (no diagonals).
    """
    return abs(node_pos[0] - goal_pos[0]) + abs(node_pos[1] - goal_pos[1])

def a_star_search(grid, start, end):
    """
    Finds the shortest path from start to end in a grid using A* algorithm.
    grid: 2D list where 0 is free, 1 is obstacle.
    start: (row, col) tuple.
    end: (row, col) tuple.
    """
    rows, cols = len(grid), len(grid[0])

    start_node = Node(start)
    end_node = Node(end)

    open_list = [] # Priority queue of nodes to be evaluated
    heapq.heappush(open_list, start_node)

    closed_list = set() # Set of nodes already evaluated

    # Store g_costs for nodes already in open_list to allow for updates
    g_costs = {start_node.position: 0}

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.position in closed_list:
            continue

        closed_list.add(current_node.position)

        if current_node == end_node:
            path = []
            curr = current_node
            while curr is not None:
                path.append(curr.position)
                curr = curr.parent
            return path[::-1] # Reverse to get path from start to end

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_pos = (current_node.position[0] + dr, current_node.position[1] + dc)

            # Check if neighbor is within grid bounds
            if not (0 <= neighbor_pos[0] < rows and 0 <= neighbor_pos[1] < cols):
                continue

            # Check if neighbor is an obstacle
            if grid[neighbor_pos[0]][neighbor_pos[1]] == 1:
                continue

            neighbor = Node(neighbor_pos, current_node)

            # Calculate g, h, and f values
            neighbor.g = current_node.g + 1 # Cost to move to neighbor is 1
            neighbor.h = heuristic(neighbor.position, end_node.position)
            neighbor.f = neighbor.g + neighbor.h

            # If neighbor is already in closed list, skip
            if neighbor.position in closed_list:
                continue

            # If a shorter path to neighbor is found, update it or add to open list
            if neighbor.position not in g_costs or neighbor.g < g_costs[neighbor.position]:
                g_costs[neighbor.position] = neighbor.g
                heapq.heappush(open_list, neighbor)

    return None # No path found

def visualize_path(grid, path):
    rows, cols = len(grid), len(grid[0])
    display_grid = [row[:] for row in grid] # Create a copy

    if path:
        for r, c in path:
            if display_grid[r][c] == 0: # Don't overwrite start/end or obstacles
                display_grid[r][c] = '*'

    for r in range(rows):
        for c in range(cols):
            if (r, c) == start_point:
                print('S', end=' ')
            elif (r, c) == end_point:
                print('G', end=' ')
            elif display_grid[r][c] == 1:
                print('#', end=' ') # Obstacle
            elif display_grid[r][c] == '*':
                print('*', end=' ')
            else:
                print('.', end=' ')
        print() # New line for each row


if __name__ == "__main__":
    # Example Grid: 0 = Free, 1 = Obstacle
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    start_point = (0, 0)
    end_point = (6, 7)

    print("Grid Map:")
    visualize_path(grid, None)

    print(f"\nFinding path from {start_point} to {end_point}...")
    path = a_star_search(grid, start_point, end_point)

    if path:
        print("\nPath Found:")
        visualize_path(grid, path)
        print(f"\nPath: {path}")
    else:
        print("\nNo path found!")

    # Test with no path
    print("\n--- Testing No Path Found ---")
    grid_no_path = [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ]
    start_no_path = (0, 0)
    end_no_path = (2, 0)
    print("Grid Map (No Path):")
    visualize_path(grid_no_path, None)
    path_no_path = a_star_search(grid_no_path, start_no_path, end_no_path)
    if path_no_path:
        print("Path Found (Error in test case!)")
    else:
        print("No path found (Correct!)")
```

### Running the Code

Run the script from your terminal: `python a_star_pathfinding.py`.

The script will first display the example grid. Then, it will calculate and print the shortest path from the start 'S' to the goal 'G', visualizing it with '*' characters. You can experiment by changing the `grid` definition, `start_point`, and `end_point` to see how the A* algorithm finds different paths or fails to find one if the goal is unreachable.

## Self-Assessment

1.  What is an "occupancy grid" used for in path planning?
2.  What is the main difference in how Dijkstra's algorithm and A* algorithm explore a graph?
3.  What role does a "heuristic" play in the A* algorithm?
4.  If the heuristic function in A* *overestimates* the cost to the goal, what can happen?
5.  In the `a_star_search` function, what is the purpose of the `open_list` and `closed_list`?

--- 

**Answer Key:**

1.  An occupancy grid represents a robot's environment as a grid of cells, each marked as either free (navigable) or occupied (obstacle), providing a discretized map for pathfinding algorithms.
2.  Dijkstra's algorithm explores outwards in all directions from the start node, guaranteeing the shortest path. A* algorithm, on the other hand, uses a heuristic to guide its search towards the goal, making it more efficient by prioritizing nodes that are likely to be on the optimal path.
3.  The heuristic provides an *estimated* cost from the current node to the goal. This estimate helps A* prioritize which nodes to explore next, guiding the search more directly towards the goal and improving efficiency.
4.  If the heuristic function in A* *overestimates* the cost to the goal (i.e., it is not admissible), the algorithm is no longer guaranteed to find the *optimal* (shortest) path. It might find a path, but it might not be the best one.
5.  The `open_list` (priority queue) stores nodes that have been discovered but not yet fully evaluated (i.e., their neighbors haven't been explored). The `closed_list` (set) stores nodes that have already been fully evaluated, preventing the algorithm from re-processing them.

## Further Reading

*   [A* Pathfinding Tutorial](https://www.redblobgames.com/pathfinding/a-star/introduction.html) - A fantastic interactive tutorial with clear explanations.
*   [Dijkstra's Algorithm](https://www.youtube.com/watch?v=Ty3gLp0W_24) - A visual explanation.
*   [Introduction to Path Planning in Robotics](https://www.youtube.com/watch?v=T6d787G1E9g) - A broader overview of path planning techniques.
