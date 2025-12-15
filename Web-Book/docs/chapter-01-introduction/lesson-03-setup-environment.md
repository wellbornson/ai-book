---
title: "Lesson 1.3: Setting Up Your Development Environment"
sidebar_position: 3
description: "A hands-on guide to installing Python, Git, and the PyBullet simulator to prepare for your robotics journey."
tags: [setup, environment, python, git, pybullet, tutorial]
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Learning Objectives

After completing this lesson, you will be able to:

*   Install Python and the Visual Studio Code IDE.
*   Set up and use Git for basic version control.
*   Install the PyBullet physics simulator using the `pip` package manager.
*   Run a "Hello, Robot!" script to verify your simulation environment is working correctly.
*   Understand the importance of virtual environments for managing project dependencies.

## Prerequisites

*   [Lesson 1.1: What is Physical AI?](./lesson-01-what-is-physical-ai.md)
*   [Lesson 1.2: Safety and Ethics in Robotics](./lesson-02-safety-and-ethics.md)
*   Administrator access on your computer to install software.

## Theory Section

### Why This Environment?

A robust development environment is a programmer's best friend. It ensures that your code runs consistently and that you have the right tools for the job. For this course, our toolkit consists of four key components:

1.  **Python:** A versatile and readable programming language that is the de facto standard in AI and robotics research. Its vast collection of libraries makes it perfect for everything from data analysis to controlling robot hardware.
2.  **Visual Studio Code (VS Code):** A modern, free, and highly extensible code editor. It provides features like syntax highlighting, code completion, and an integrated terminal, which streamlines the development process.
3.  **Git:** The industry-standard version control system. Git allows you to track changes to your code, collaborate with others, and revert to previous versions if something breaks. It's like a "save game" system for your projects.
4.  **PyBullet:** A fast and easy-to-use physics simulator. Simulation is a crucial tool in robotics. It allows us to design, test, and debug our robots in a safe, cost-effective, and virtual environment before ever touching physical hardware.

### The Importance of Virtual Environments

When you work on multiple Python projects, you'll find that they may have different dependencies (i.e., they require different versions of a library). A **virtual environment** is an isolated directory that contains a specific version of Python and all the libraries required for a particular project.

Using virtual environments prevents conflicts and ensures your project is self-contained and reproducible. We will use Python's built-in `venv` module to manage our environment for this course.

## Practical Section: Step-by-Step Setup

Follow these instructions carefully for your operating system.

### Step 1: Install Python and VS Code

First, install Python and the VS Code editor.

1.  **Install Python 3.8+:**
    *   Go to the official [Python download page](https://www.python.org/downloads/).
    *   Download and run the installer for the latest stable version of Python (3.8 or higher).
    *   **On Windows:** During installation, make sure to check the box that says **"Add Python to PATH"**. This is very important!

2.  **Install Visual Studio Code:**
    *   Go to the [VS Code download page](https://code.visualstudio.com/download).
    *   Download and run the installer for your operating system.

3.  **Install the Python Extension for VS Code:**
    *   Open VS Code.
    *   Go to the Extensions view by clicking the icon in the sidebar on the left.
    *   Search for "Python" (by Microsoft) and click **Install**.

### Step 2: Install and Configure Git

Git is essential for managing your code.

<Tabs>
  <TabItem value="windows" label="Windows">
    <p>
      Download and install <strong>Git for Windows</strong> from <a href="https://git-scm.com/download/win">git-scm.com</a>. The default options during installation are fine for our purposes. This will also give you Git Bash, a useful terminal for running commands.
    </p>
  </TabItem>
  <TabItem value="mac" label="macOS">
    <p>
      The easiest way is to install Xcode Command Line Tools. Open the Terminal app and run:
      <br/>
      <code>xcode-select --install</code>
      <br/>
      This will install Git automatically.
    </p>
  </TabItem>
  <TabItem value="linux" label="Linux">
    <p>
      Open your terminal and use your distribution's package manager. For Debian/Ubuntu:
      <br/>
      <code>sudo apt update && sudo apt install git</code>
    </p>
  </TabItem>
</Tabs>

After installation, introduce yourself to Git by running these commands in your terminal (use your actual name and email):

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Create Your Project and Virtual Environment

Now, let's set up the project folder and the virtual environment.

1.  **Create a Project Folder:** Create a folder for this course, for example `physical-ai-course`.
2.  **Open in VS Code:** Open the `physical-ai-course` folder in VS Code (`File > Open Folder...`).
3.  **Open the Terminal:** Use the integrated terminal in VS Code (`Terminal > New Terminal`).

4.  **Create the Virtual Environment:** In the VS Code terminal, run the following command. This creates a sub-directory named `venv` which will contain our isolated Python environment.

    ```bash
    python -m venv venv
    ```

5.  **Activate the Virtual Environment:** You must activate the environment before you can use it.

    <Tabs>
      <TabItem value="windows" label="Windows (PowerShell)">
        <p><code>.\venv\Scripts\Activate.ps1</code></p>
        <p>If you get an error about execution policies, you may need to run <code>Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process</code> and then try activating again.</p>
      </TabItem>
      <TabItem value="maclinux" label="macOS / Linux">
        <p><code>source venv/bin/activate</code></p>
      </TabItem>
    </Tabs>

    When the environment is active, your terminal prompt will change to show `(venv)`. You are now "inside" the virtual environment.

### Step 4: Install PyBullet

With the virtual environment active, install PyBullet using `pip`, Python's package installer.

```bash
pip install pybullet
```

`pip` will automatically download and install PyBullet into your `venv`, leaving your global Python installation clean.

## Code Example: "Hello, Robot!"

You are now ready to run your first simulation!

1.  **Create a File:** In VS Code's file explorer, create a new file named `hello_robot.py`.
2.  **Add the Code:** Copy and paste the following code into the file.
3.  **Run the Code:** Make sure your `(venv)` is still active in the terminal, then run the script with the command: `python hello_robot.py`

```python title="hello_robot.py"
import pybullet as p
import time
import pybullet_data

# 1. Connect to the Physics Engine
# Use p.GUI to create a window, or p.DIRECT for a non-graphical instance
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath()) # Varies by machine

# 2. Setup the Simulation
p.setGravity(0, 0, -9.81)  # Set gravity
planeId = p.loadURDF("plane.urdf") # Load a ground plane

# Set the starting position and orientation for the robot
startPos = [0, 0, 1]
startOrientation = p.getQuaternionFromEuler([0, 0, 0])

# 3. Load a Robot Model
# PyBullet includes some basic models. URDF files define robot properties.
robotId = p.loadURDF("r2d2.urdf", startPos, startOrientation)
print("Hello, Robot! My ID is:", robotId)

# 4. Run the Simulation
# The simulation runs in steps. We can loop to advance it over time.
for i in range(10000):
    p.stepSimulation() # Advance the simulation by one step
    time.sleep(1./240.) # Control the simulation speed (e.g., 240 steps per second)

# 5. Disconnect
p.disconnect()
print("Simulation finished.")

```

When you run the script, a new window should appear showing an R2-D2 model falling onto a plane. This confirms that your environment is set up correctly!

## Self-Assessment

1.  Why do we use a virtual environment?
2.  What command do you use to install a Python package with `pip`?
3.  What does the `git config` command do?
4.  In the `hello_robot.py` script, what is the difference between `p.GUI` and `p.DIRECT`?
5.  What file format is used to define the R2-D2 robot model in the script?

---

**Answer Key:**

1.  We use a virtual environment to isolate project dependencies, preventing conflicts between projects that might require different versions of the same library.
2.  `pip install <package_name>`
3.  The `git config` command is used to set configuration options for Git, such as your username and email, which are attached to every commit you make.
4.  `p.GUI` connects to the physics engine and opens a graphical window to visualize the simulation. `p.DIRECT` connects without a GUI, which is useful for running simulations quickly in the background (e.g., on a server or for batch processing).
5.  The file format is **URDF** (Unified Robot Description Format). The file is `r2d2.urdf`.

## Further Reading

*   [VS Code "Getting Started with Python" Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
*   [Official Python `venv` Documentation](https://docs.python.org/3/library/venv.html)
*   [PyBullet Quickstart Guide](https://pybullet.org/wordpress/index.php/2020/04/01/pybullet-quickstart-guide/)
