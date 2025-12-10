# Quickstart Guide: Physical AI Book Development

**Purpose**: Get up and running with the Docusaurus course site in under 30 minutes
**Last Updated**: 2025-12-06
**Prerequisites**: Basic command line knowledge, Git installed

## Overview

This guide walks you through:
1. Setting up your development environment
2. Initializing the Docusaurus project
3. Creating your first lesson
4. Building and deploying the site

**Estimated Time**: 20-30 minutes

---

## Step 1: Install Prerequisites

### Required Software

1. **Node.js 18+** and **npm**
   - Download from: https://nodejs.org/
   - Verify installation:
     ```bash
     node --version  # Should be v18.0.0 or higher
     npm --version   # Should be 9.0.0 or higher
     ```

2. **Python 3.8+** (for code examples)
   - Download from: https://www.python.org/downloads/
   - Verify installation:
     ```bash
     python --version  # or python3 --version
     # Should be 3.8.0 or higher
     ```

3. **Git** (for version control)
   - Download from: https://git-scm.com/
   - Verify installation:
     ```bash
     git --version
     ```

### Optional but Recommended

- **VS Code** with extensions:
  - Markdown All in One
  - Docusaurus Snippets
  - Python
- **draw.io Desktop** (for creating diagrams)

---

## Step 2: Initialize Docusaurus Project

### Create New Docusaurus Site

```bash
# Navigate to your project directory
cd C:\Users\wellbornsonAi\Desktop\Web-Book

# Initialize Docusaurus using classic template
npx create-docusaurus@latest docs classic

# Navigate into the created directory
cd docs
```

**What This Creates**:
- `docusaurus.config.js` - Main configuration
- `sidebars.js` - Sidebar navigation structure
- `docs/` - Content directory (Markdown files)
- `src/` - Custom components and pages
- `static/` - Static assets (images, files)
- `package.json` - Node dependencies

### Install Dependencies

```bash
npm install
```

### Test Local Development Server

```bash
npm start
```

Your browser should open to `http://localhost:3000` showing the default Docusaurus site.

**Press `Ctrl+C` to stop the server when ready to continue.**

---

## Step 3: Configure Site for Course

### Update `docusaurus.config.js`

Open `docusaurus.config.js` and update these key sections:

```javascript
// @ts-check
const {themes} = require('prism-react-renderer');
const lightTheme = themes.github;
const darkTheme = themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics Course',
  tagline: 'Learn robotics from foundations to advanced topics',
  favicon: 'img/favicon.ico',

  url: 'https://your-site-url.com',  // Replace with your domain
  baseUrl: '/',

  organizationName: 'your-org',  // Usually your GitHub org/user name
  projectName: 'physical-ai-course',  // Usually your repo name

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/your-org/physical-ai-course/tree/main/',
          routeBasePath: '/',  // Serve docs at site root
        },
        blog: false,  // Disable blog (optional)
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/social-card.png',
      navbar: {
        title: 'Physical AI Course',
        logo: {
          alt: 'Course Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Course Content',
          },
          {
            href: 'https://github.com/your-org/physical-ai-course',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Course',
            items: [
              {
                label: 'Getting Started',
                to: '/',
              },
              {
                label: 'About',
                to: '/about',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/your-org/physical-ai-course',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI Course. Built with Docusaurus.`,
      },
      prism: {
        theme: lightTheme,
        darkTheme: darkTheme,
        additionalLanguages: ['python', 'bash'],
      },
      algolia: {  // Optional: Algolia DocSearch for advanced search
        appId: 'YOUR_APP_ID',
        apiKey: 'YOUR_API_KEY',
        indexName: 'physical-ai-course',
      },
    }),
};

module.exports = config;
```

---

## Step 4: Create Course Structure

### Set Up Chapter Directories

```bash
# Navigate to docs/ directory
cd docs

# Create directories for all 10 chapters
mkdir chapter-01-introduction
mkdir chapter-02-sensors
mkdir chapter-03-actuators
mkdir chapter-04-kinematics
mkdir chapter-05-control
mkdir chapter-06-path-planning
mkdir chapter-07-machine-learning
mkdir chapter-08-manipulation
mkdir chapter-09-humanoid
mkdir chapter-10-integration

# Create directories for static assets
cd ../static
mkdir -p img/chapter-01 img/chapter-02 img/chapter-03 img/chapter-04 img/chapter-05 img/chapter-06 img/chapter-07 img/chapter-08 img/chapter-09 img/chapter-10
mkdir -p img/sources
mkdir -p code-examples/chapter-01 code-examples/chapter-02 code-examples/chapter-03
# ... (repeat for remaining chapters)

# Navigate back to project root
cd ..
```

### Configure Sidebar (`sidebars.js`)

Replace contents of `sidebars.js`:

```javascript
// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'index',
      label: 'Course Home',
    },
    {
      type: 'category',
      label: 'Chapter 1: Introduction',
      link: {
        type: 'generated-index',
        description: 'Foundational concepts introducing students to physical AI and robotics.',
      },
      items: [
        'chapter-01-introduction/lesson-01-what-is-physical-ai',
        'chapter-01-introduction/lesson-02-safety-and-ethics',
        'chapter-01-introduction/lesson-03-setup-environment',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 2: Sensors',
      link: {
        type: 'generated-index',
        description: 'Explore how robots perceive their environment through sensors.',
      },
      items: [
        'chapter-02-sensors/lesson-01-sensor-fundamentals',
        'chapter-02-sensors/lesson-02-vision-sensors',
        'chapter-02-sensors/lesson-03-lidar-depth-multimodal',
      ],
    },
    // Add remaining chapters (3-10) following the same pattern
  ],
};

module.exports = sidebars;
```

---

## Step 5: Create Your First Lesson

### Copy Lesson Template

```bash
# Copy the lesson template to Chapter 1, Lesson 1
cp specs/001-book-structure/contracts/lesson-template.md docs/chapter-01-introduction/lesson-01-what-is-physical-ai.md
```

### Fill In Template Placeholders

Open `docs/chapter-01-introduction/lesson-01-what-is-physical-ai.md` and replace placeholders:

```markdown
---
title: "Lesson 1.1: What is Physical AI?"
sidebar_position: 1
description: "Introduction to physical AI concepts, real-world applications, and distinctions from virtual AI systems."
tags: [introduction, foundations, physical-ai, robotics]
---

# Lesson 1.1: What is Physical AI?

:::tip Estimated Time
⏱️ **45 minutes** to complete this lesson
:::

## Learning Objectives

By the end of this lesson, you will be able to:

- **Define Physical AI**: Explain what physical AI is and how it differs from traditional AI
- **Identify Applications**: Recognize real-world applications of physical AI in various industries
- **Understand Components**: Describe the key components that make up a physical AI system
- **Distinguish Virtual vs. Physical**: Compare and contrast physical AI with virtual AI systems

## Prerequisites

This is the first lesson in the course - no prerequisites required!

**Assumed Knowledge**:
- Basic programming concepts (variables, functions, loops)
- Familiarity with using a computer and command line

:::note Starting Fresh?
No robotics or AI experience needed! We'll start from the very beginning.
:::

---

## Theory

### Introduction

Imagine a robot that can see, touch, move, and interact with the world around it - that's Physical AI. Unlike chatbots or recommendation algorithms that exist purely in software, physical AI systems have a body. They use sensors to perceive their environment and actuators to take action in the real world.

**Why does this matter?** Physical AI is transforming industries: manufacturing robots assemble cars, surgical robots assist doctors, and autonomous vehicles navigate roads. Understanding physical AI opens doors to building systems that don't just process information, but physically change the world.

### What is Physical AI?

**Physical AI** (also called **Embodied AI**) is artificial intelligence that interacts with the physical world through a robot body. It combines:

1. **Perception**: Sensors gather information (cameras see, touch sensors feel, microphones hear)
2. **Cognition**: AI algorithms process sensor data and make decisions
3. **Action**: Actuators execute decisions (motors move joints, grippers grasp objects)

![Physical AI system showing perception-cognition-action loop](../../../static/img/chapter-01/figure-11-physical-ai-loop.svg)

**Figure 1.1**: Physical AI system demonstrating the perception-cognition-action cycle.

### Physical AI vs. Virtual AI

| Aspect | Virtual AI | Physical AI |
|--------|-----------|-------------|
| **Embodiment** | Exists only in software | Has a physical robot body |
| **Interaction** | Processes digital data | Interacts with real world |
| **Sensors** | Keyboard, mouse, APIs | Cameras, touch, force sensors |
| **Actions** | Display results, send data | Move, manipulate objects |
| **Examples** | ChatGPT, recommendation systems | Humanoid robots, self-driving cars |

### Real-World Applications

**Manufacturing**: Assembly line robots weld car frames, pick and place components, and perform quality inspection 24/7 with precision.

**Healthcare**: Surgical robots like da Vinci enable minimally invasive procedures. Rehabilitation robots help patients regain mobility after injury.

**Exploration**: Mars rovers like Perseverance navigate alien terrain, collect samples, and search for signs of life where humans cannot go.

**Everyday Life**: Robot vacuums navigate homes, delivery robots bring food, and assistive robots help elderly individuals with daily tasks.

:::tip Key Takeaway
Physical AI bridges the gap between digital intelligence and the physical world, enabling AI to not just think, but to see, move, and interact with reality.
:::

---

## Hands-On Practice

### Exercise Overview

**Goal**: Understand the components of a physical AI system by identifying them in real-world examples

**What You'll Need**:
- Pen and paper (or digital note-taking app)
- Internet access to watch videos

### Step 1: Watch Robot Demonstrations

Watch these short videos (5-7 minutes total):

1. Boston Dynamics Atlas robot: [YouTube search "Boston Dynamics Atlas"]
2. Tesla Optimus robot: [YouTube search "Tesla Optimus Gen 2"]
3. Any robotic arm video: [YouTube search "industrial robot arm"]

### Step 2: Identify Components

For each video, identify:

- **Sensors**: What sensors does the robot likely use? (cameras, touch, balance sensors)
- **Actuators**: What moves? (joints, grippers, wheels)
- **Tasks**: What is the robot doing? (walking, grasping, assembling)

### Step 3: Reflection

Answer these questions:

1. How does the robot perceive its environment?
2. What actions can it take?
3. What challenges might it face in the real world? (uneven terrain, unexpected obstacles, etc.)

:::warning Common Pitfall
Don't confuse computer graphics simulations with real robots! Physical AI must deal with real-world physics, friction, and uncertainty that simulations often simplify.
:::

---

## Code Examples

### Minimal Example: Hello Robot (Conceptual)

This lesson is conceptual (no coding yet). In Lesson 1.3, you'll set up your environment and write your first robot simulation!

**Preview**: Here's what a simple robot simulation looks like:

```python
# Preview: Coming in Lesson 1.3
import pybullet as p

p.connect(p.GUI)  # Open simulation window
p.setGravity(0, 0, -9.81)  # Set Earth gravity

# Create a simple robot...
# (Full code in Lesson 1.3)

p.disconnect()
```

**What This Will Do**: Opens a 3D simulation environment where you can create and control virtual robots before working with physical hardware.

---

## Self-Assessment

:::tip Success Criteria
Complete at least **3 out of 4** questions correctly to demonstrate mastery of this lesson's objectives.
:::

### Question 1: Multiple Choice

What is the key distinction between Physical AI and Virtual AI?

A) Physical AI is more intelligent
B) Physical AI interacts with the physical world through a robot body
C) Virtual AI is faster
D) Physical AI doesn't use software

<details>
<summary>Click to reveal answer</summary>

**Answer**: B

**Explanation**: Physical AI (embodied AI) has a physical robot body with sensors and actuators that allow it to perceive and interact with the real world, unlike virtual AI which exists purely in software.

</details>

---

### Question 2: True or False

A chatbot like ChatGPT is an example of Physical AI because it uses AI algorithms.

<details>
<summary>Click to reveal answer</summary>

**Answer**: False

**Explanation**: ChatGPT is Virtual AI - it processes text but has no physical body, sensors, or actuators. Physical AI requires embodiment (a robot body) to interact with the physical world.

</details>

---

### Question 3: Short Answer / Reflection

Describe one real-world application of Physical AI and explain why it requires a physical body rather than just software.

<details>
<summary>Sample Answer</summary>

A strong answer should include:
- Specific application (e.g., surgical robot, Mars rover, manufacturing robot)
- Why physical interaction is necessary (manipulate objects, navigate terrain, interact with patients)
- Sensors and actuators involved

**Example Response**: "A surgical robot like da Vinci assists doctors in minimally invasive surgery. It requires a physical body because it must physically manipulate surgical tools, apply precise forces to tissue, and navigate inside the human body. Cameras provide visual feedback, force sensors detect resistance, and actuators control tool movements with sub-millimeter precision - tasks impossible for pure software."

</details>

---

### Question 4: Application Analysis

Watch a video of any robot (search YouTube for "robot demonstration"). List 3 sensors and 3 actuators you think the robot uses.

<details>
<summary>Sample Answer</summary>

**Example for Boston Dynamics Atlas**:

Sensors (likely):
1. Cameras for visual perception
2. IMU (Inertial Measurement Unit) for balance
3. Joint encoders to track limb positions

Actuators:
1. Electric motors in leg joints for walking
2. Torso actuators for balance adjustments
3. Arm motors for manipulation

Your answer will vary based on the robot you watched, but the key is identifying how it senses (cameras, touch, position) and acts (motors, grippers, wheels).

</details>

---

## Further Reading

Want to dive deeper? Check out these resources:

### Articles & Blogs
- [What is Embodied AI?](https://blogs.nvidia.com/blog/what-is-embodied-ai/) - NVIDIA Blog explaining embodied AI
- [Physical AI vs. Digital AI](https://example.com) - Comparison article

### Video Resources
- [How Do Robots See?](https://youtube.com/watch?v=example) - Explanation of robot vision
- [Boston Dynamics Behind the Scenes](https://youtube.com/watch?v=example) - Engineering insights

### Academic (Optional)
- "Embodied Artificial Intelligence" by Rolf Pfeifer - Foundational book on the topic

:::tip Next Steps
Ready to continue? Head to [Lesson 1.2: Safety and Ethics in Robotics](./lesson-02-safety-and-ethics.md) to learn about working safely and responsibly with physical AI systems.
:::

---

## Lesson Summary

In this lesson, you learned:

- ✅ Physical AI combines perception, cognition, and action through a robot body
- ✅ Physical AI differs from Virtual AI by having sensors, actuators, and real-world interaction
- ✅ Applications span manufacturing, healthcare, exploration, and everyday life
- ✅ The perception-cognition-action loop is fundamental to physical AI systems

**Key Concepts Covered**:
- Definition of Physical AI (Embodied AI)
- Components: sensors, actuators, AI algorithms
- Real-world applications and their requirements

**Practical Skills Gained**:
- Identifying sensors and actuators in robot systems
- Distinguishing physical vs. virtual AI
- Analyzing robot capabilities and limitations

These foundational concepts prepare you for understanding robot sensors (Chapter 2), actuators (Chapter 3), and building your own robotic systems!

---

**Questions or Feedback?** [Open an issue on GitHub](https://github.com/your-org/physical-ai-course/issues) or discuss in the community forum.
```

---

## Step 6: Build and Test

### Build the Site

```bash
# From project root
npm run build
```

This creates a `build/` directory with static HTML files.

### Test Production Build

```bash
npm run serve
```

Navigate to `http://localhost:3000` to view the production build.

---

## Step 7: Version Control with Git

### Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial Docusaurus setup for Physical AI Course"
```

### Create `.gitignore`

Ensure your `.gitignore` includes:

```
# Dependencies
node_modules/

# Production
build/

# Generated files
.docusaurus/
.cache/

# Misc
.DS_Store
Thumbs.db

# Editor directories
.vscode/
.idea/

# Python
__pycache__/
*.pyc
venv/
*.egg-info/
```

### Connect to GitHub (Optional)

```bash
git remote add origin https://github.com/your-org/physical-ai-course.git
git branch -M main
git push -u origin main
```

---

## Step 8: Deploy (Optional)

### Deploy to GitHub Pages

1. Install GitHub Pages plugin:
   ```bash
   npm install @docusaurus/plugin-gh-pages --save
   ```

2. Update `docusaurus.config.js`:
   ```javascript
   url: 'https://your-username.github.io',
   baseUrl: '/physical-ai-course/',
   organizationName: 'your-username',
   projectName: 'physical-ai-course',
   ```

3. Deploy:
   ```bash
   GIT_USER=your-username npm run deploy
   ```

### Alternative: Deploy to Netlify/Vercel

- **Netlify**: Connect GitHub repo, build command `npm run build`, publish directory `build/`
- **Vercel**: Similar process, auto-detects Docusaurus

---

## Next Steps

Now that you have a working Docusaurus site:

1. **Create Remaining Lessons**: Use the lesson template to create all 30 lessons
2. **Add Chapter Category Configs**: Create `_category_.json` files for each chapter using the schema
3. **Develop Content**: Follow the content development workflow (outline → draft → code → integrate → review → test → refine)
4. **Add Code Examples**: Create Python code examples in `static/code-examples/`
5. **Create Diagrams**: Use draw.io to create SVG diagrams in `static/img/`

### Helpful Commands

- `npm start` - Start development server
- `npm run build` - Build production site
- `npm run serve` - Preview production build
- `npm run clear` - Clear cache (if experiencing issues)
- `npm run write-translations` - Extract translatable strings (for i18n)

### Resources

- **Docusaurus Docs**: https://docusaurus.io/docs
- **Markdown Guide**: https://www.markdownguide.org/
- **Lesson Template**: `specs/001-book-structure/contracts/lesson-template.md`
- **Constitution**: `.specify/memory/constitution.md`

---

## Troubleshooting

### Common Issues

**"Module not found" errors**:
```bash
rm -rf node_modules package-lock.json
npm install
```

**Port 3000 already in use**:
```bash
# Specify different port
npm start -- --port 3001
```

**Build fails with broken links**:
- Check all internal links use correct paths
- Verify all referenced files exist
- Run `npm run build` to see specific errors

**Code examples don't run**:
- Verify Python 3.8+ installed
- Check virtual environment is activated
- Ensure all dependencies in `requirements.txt` are installed

---

## Success Checklist

- [ ] Node.js 18+ and Python 3.8+ installed
- [ ] Docusaurus project initialized
- [ ] Site configuration updated
- [ ] Chapter directories created
- [ ] Sidebar configured
- [ ] First lesson created from template
- [ ] Site builds and runs locally (`npm start`)
- [ ] Git repository initialized
- [ ] Ready to develop remaining content!

**Congratulations!** You're ready to start building the Physical AI & Humanoid Robotics Course. Refer to `plan.md` for the full implementation roadmap.
