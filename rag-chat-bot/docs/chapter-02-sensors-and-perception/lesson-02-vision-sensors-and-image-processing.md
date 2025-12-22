---
title: "Lesson 2.2: Vision Sensors and Image Processing"
sidebar_position: 2
description: "A primer on how robots 'see' using cameras, from pixels and color spaces to real-time image processing with OpenCV."
tags: [sensors, vision, camera, opencv, image-processing]
---

## Learning Objectives

After completing this lesson, you will be able to:

*   Explain how a camera works as a sensor for a robot.
*   Understand how images are represented digitally (pixels, color spaces).
*   Perform basic image processing tasks like color filtering and edge detection.
*   Use the OpenCV library in Python to capture and manipulate image data from a simulated camera.
*   Appreciate the challenges and opportunities of using vision in robotics.

## Prerequisites

*   [Lesson 2.1: Sensor Fundamentals](./lesson-01-sensor-fundamentals.md)
*   A working Python and PyBullet environment from Chapter 1.

## Theory Section

### The Richest Sensor of All

Of all the sensors available to a robot, the **camera** is arguably the most powerful. Vision provides an immense amount of rich, dense information about the environment. A single image can tell a robot about the presence of objects, their shape, color, texture, and location relative to each other.

For a robot, "seeing" is a two-step process:
1.  **Image Capture:** A camera captures light from the world and converts it into a digital image.
2.  **Image Processing:** An algorithm processes this image to extract meaningful information.

This lesson focuses on the fundamentals of both steps.

### How Digital Images Work

#### Pixels
A digital image is not a continuous picture. It's a grid of tiny, discrete elements called **pixels** (short for "picture elements"). Each pixel has a specific location (an X and Y coordinate) and a specific color. The resolution of an image (e.g., 1920x1080) refers to the number of pixels in its grid (width x height).

#### Color Spaces
How is a pixel's color stored? The most common method is the **RGB (Red, Green, Blue)** color model. The color of each pixel is represented by three numbers, indicating the intensity of red, green, and blue light. Each number typically ranges from 0 (no intensity) to 255 (full intensity).

*   `[255, 0, 0]` is pure Red.
*   `[0, 255, 0]` is pure Green.
*   `[0, 0, 0]` is Black.
*   `[255, 255, 255]` is White.
*   `[255, 255, 0]` is Yellow (a mix of red and green).

While RGB is great for displays, it's not always ideal for computer vision. For example, trying to find all the "red" objects in an image is difficult because shadows and lighting can dramatically change the RGB values.

For this reason, computer vision practitioners often use other color spaces, like **HSV (Hue, Saturation, Value)**.
*   **Hue:** The "pure" color (e.g., red, green, blue, yellow). It's represented as an angle from 0-360 degrees.
*   **Saturation:** The "richness" or "purity" of the color. 0 is grayscale, and max saturation is the purest color.
*   **Value:** The "brightness" or "intensity" of the color. 0 is black.

The key advantage of HSV is that the color (Hue) is separated from the brightness (Value). This makes it much more robust for finding objects of a certain color regardless of lighting conditions.

![HSV Color Space](https://i.imgur.com/gpl7fEk.png)
*Figure 1: The HSV color space separates color (Hue) from intensity (Value), making it robust to lighting changes.*

### Introducing OpenCV

**OpenCV (Open Source Computer Vision Library)** is the world's most popular library for computer vision. It provides thousands of optimized algorithms for real-time image and video processing. We will use `opencv-python`, the Python wrapper for the library, to perform our image processing tasks.

### Basic Image Processing Techniques

1.  **Color Filtering (or Color Thresholding):**
    This is the process of creating a **binary mask** from an image, where we make pixels that are within a certain color range white, and all other pixels black. This is an easy way to isolate an object of a specific color. This technique is extremely powerful when using the HSV color space.

2.  **Edge Detection:**
    Edges are one of the most important features in an image. They represent boundaries between objects or parts of objects. The **Canny edge detector** is a popular and effective multi-stage algorithm for finding edges. It identifies areas with sharp changes in intensity and produces a clean, one-pixel-thick line representing the edge.

## Practical Section

In this exercise, we will use PyBullet to simulate a camera and OpenCV to process the images it captures. We will perform color filtering to find a specific object (a red ball) in the scene.

### Step 1: Install OpenCV

Before running the code, you need to install `opencv-python` and `numpy` (a library for numerical operations that OpenCV depends on). In your VS Code terminal with your `(venv)` activated, run:

```bash
pip install opencv-python numpy
```

### Step 2: The Code

Create a new Python file named `vision_processing.py` and copy the code below into it.

Read through the code and the comments to understand each step. We set up a scene with a few objects, position a camera, and then enter a loop. In each step of the loop, we:
1.  Get an image from the simulated camera.
2.  Convert the image from RGB to HSV.
3.  Define a color range for "red" and create a mask.
4.  Display the original camera feed and the binary mask.

```python title="vision_processing.py"
import pybullet as p
import time
import pybullet_data
import cv2
import numpy as np

# --- PyBullet Setup ---
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Load models
planeId = p.loadURDF("plane.urdf")
# Load a table and some objects
p.loadURDF("table/table.urdf", useFixedBase=True, basePosition=[0, 0, 0])
red_ball = p.loadURDF("sphere_small.urdf", basePosition=[0.5, 0, 0.7], globalScaling=1.5)
blue_cube = p.loadURDF("cube_small.urdf", basePosition=[-0.5, 0, 0.7])

# Change the color of the objects
p.changeVisualShape(red_ball, -1, rgbaColor=[1, 0, 0, 1])
p.changeVisualShape(blue_cube, -1, rgbaColor=[0, 0, 1, 1])

# --- Camera Setup ---
# We need to define the camera's properties
view_matrix = p.computeViewMatrix(
    cameraEyePosition=[0, -3, 2],
    cameraTargetPosition=[0, 0, 0.5],
    cameraUpVector=[0, 0, 1])

projection_matrix = p.computeProjectionMatrixFOV(
    fov=45.0,
    aspect=1.0,
    nearVal=0.1,
    farVal=3.1)

# --- Main Loop ---
while True:
    # 1. Get Image from PyBullet Camera
    width, height, rgb_img, depth_img, seg_img = p.getCameraImage(
        width=224,
        height=224,
        viewMatrix=view_matrix,
        projectionMatrix=projection_matrix)

    # PyBullet returns a 1D array, reshape it to a 2D image
    # Also, drop the alpha channel (4th channel)
    rgb_img = np.reshape(rgb_img, (height, width, 4))[:, :, :3]

    # 2. Convert from RGB to HSV
    hsv_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)

    # 3. Define the color range for RED and create a mask
    # These values might need tuning depending on the lighting!
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    # You often need two ranges for red because it wraps around 0/180 in HSV
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv_img, lower_red, upper_red)
    mask2 = cv2.inRange(hsv_img, lower_red2, upper_red2)
    mask = mask1 + mask2 # Combine the two masks

    # 4. Display the results using OpenCV
    # OpenCV uses BGR format, so we need to convert RGB to BGR for display
    bgr_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)
    cv2.imshow("Camera Feed", bgr_img)
    cv2.imshow("Red Object Mask", mask)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    p.stepSimulation()
    time.sleep(1./240.)

# Cleanup
cv2.destroyAllWindows()
p.disconnect()
```

### Step 3: Run the Code

In your VS Code terminal, run the script:

```bash
python vision_processing.py
```

Two windows should appear:
1.  **"Camera Feed"**: Shows the robot's view of the scene.
2.  **"Red Object Mask"**: This is the result of our color filtering. It should be a black image with a white circle where the red ball is located.

Press 'q' with one of the OpenCV windows selected to close the simulation.

## Self-Assessment

1.  What is the difference between an image's resolution and its color depth?
2.  What is the primary advantage of using the HSV color space over RGB for object detection?
3.  What is a "binary mask" in the context of image processing?
4.  In the code example, why do we need two different ranges for the color red?
5.  What does the `cv2.imshow()` function do?

---

**Answer Key:**

1.  **Resolution** is the number of pixels in the image grid (e.g., 640x480). **Color depth** is the amount of information stored for each pixel (e.g., an 8-bit RGB image uses 24 bits per pixel).
2.  HSV separates color (Hue) from brightness/intensity (Value). This makes color-based detection more robust to changes in lighting.
3.  A binary mask is an image where each pixel is either "on" (typically white) or "off" (typically black). It's used to represent the result of a filtering operation, showing which pixels in the original image met the criteria.
4.  In the standard HSV color model, the hue for "red" is at the very beginning and end of the range (0 and 180 in OpenCV's scale). So, to capture all shades of red, we need to check for values near 0 and values near 180.
5.  The `cv2.imshow()` function displays an image in a window. The first argument is the window name, and the second is the image (as a NumPy array) to be displayed.

## Further Reading

*   [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) - The official documentation is a great place to start.
*   [Color Thresholding with OpenCV](https://www.pyimagesearch.com/2021/01/19/opencv-bitwise-and-or-xor-and-not/) - A practical guide from PyImageSearch.
*   [Computerphile: Canny Edge Detector](https://www.youtube.com/watch?v=uWXslI0Qk3A) - A great video explaining how the Canny algorithm works.
