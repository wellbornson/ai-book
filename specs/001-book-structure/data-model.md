# Data Model: Physical AI Book Structure

**Feature**: 001-book-structure
**Date**: 2025-12-06
**Purpose**: Define key entities, relationships, and data structures for the course content

## Entity Definitions

### 1. Chapter

**Description**: A major topic area containing 3 related lessons, representing a cohesive unit of learning.

**Attributes**:
- `number` (integer, 1-10): Chapter sequence number
- `title` (string): Descriptive chapter title (e.g., "Introduction to Physical AI and Robotics")
- `slug` (string): URL-friendly identifier (e.g., "chapter-01-introduction")
- `description` (string, 100-300 chars): Brief summary of chapter content and goals
- `learningOutcomes` (array of strings): 3-5 high-level skills students gain from this chapter
- `estimatedHours` (float): Expected time for students to complete chapter (3-6 hours)
- `difficulty` (enum: "beginner", "intermediate", "advanced"): Difficulty level
- `prerequisites` (array of chapter slugs): Chapters that should be completed first
- `position` (integer): Sidebar display order (matches number)
- `collapsed` (boolean): Whether chapter is collapsed in sidebar by default

**Relationships**:
- Has many (3): Lessons
- Has many: Visual Assets (diagrams specific to chapter intro)
- Has one: Category Config File (`_category_.json`)

**Validation Rules**:
- Each chapter MUST have exactly 3 lessons
- `number` MUST be unique and sequential (1-10)
- `slug` MUST follow pattern `chapter-##-{topic}` (e.g., `chapter-01-introduction`)
- `learningOutcomes` MUST contain 3-5 items

**File Representation**:
```json
// docs/chapter-##-{slug}/_category_.json
{
  "label": "Chapter {number}: {title}",
  "position": {number},
  "link": {
    "type": "generated-index",
    "description": "{description}"
  },
  "collapsed": false
}
```

---

### 2. Lesson

**Description**: Individual learning unit containing all 8 mandatory components per constitution.

**Attributes**:
- `number` (integer, 1-3): Lesson number within chapter
- `chapterNumber` (integer): Parent chapter
- `title` (string): Descriptive lesson title (e.g., "What is Physical AI?")
- `slug` (string): Filename without extension (e.g., "lesson-01-what-is-physical-ai")
- `description` (string, 50-150 chars): One-sentence summary for search and meta tags
- `tags` (array of strings): Topic tags for search and filtering
- `estimatedMinutes` (integer): Expected completion time (30-90 minutes)
- `difficulty` (enum): "beginner", "intermediate", "advanced"
- `sidebarPosition` (integer): Display order within chapter (1-3)
- `prerequisites` (array of lesson slugs): Lessons that should be completed first
- `learningObjectives` (array of strings): 3-5 specific, measurable outcomes
- `hasSafetyContent` (boolean): Whether lesson includes safety warnings
- `hasCodeExamples` (boolean): Whether lesson includes executable code
- `assessmentType` (enum): "quiz", "reflection", "mini-project", "mixed"

**Relationships**:
- Belongs to: Chapter
- Has many: Code Examples (0-5 per lesson)
- Has many: Visual Assets (diagrams, images)
- Has one: Assessment
- References many: Prerequisites (other lessons)

**Validation Rules**:
- Lesson MUST belong to exactly one chapter
- Lesson MUST include all 8 mandatory components:
  1. Title and Metadata (front matter)
  2. Learning Objectives (3-5 bullets)
  3. Prerequisites (list with links)
  4. Theory Section (beginner → technical)
  5. Practical Section (step-by-step)
  6. Code Examples (complete, runnable, commented)
  7. Safety Considerations (conditional: if `hasSafetyContent`)
  8. Self-Assessment (quiz/questions/project)
  9. Further Reading (optional resources)
- `number` MUST be 1, 2, or 3 within chapter
- `learningObjectives` MUST contain 3-5 specific, testable outcomes
- If `hasSafetyContent` is true, Safety Considerations section MUST be present

**File Representation**:
```markdown
---
title: "Lesson {chapter}.{number}: {title}"
sidebar_position: {sidebarPosition}
description: "{description}"
tags: {tags}
---

# Lesson {chapter}.{number}: {title}

## Learning Objectives

- Objective 1 (specific, measurable)
- Objective 2
- Objective 3

## Prerequisites

- [Lesson X.Y: Title](../chapter-XX/lesson-YY-slug.md)

## Theory

[Jargon-free introduction...]

[Progressive technical depth...]

## Hands-On Practice

[Step-by-step exercise instructions...]

## Code Examples

[Complete, runnable, commented Python code...]

## Safety Considerations

[Explicit warnings and precautions - if applicable...]

## Self-Assessment

[Quiz, reflection questions, or mini-project...]

## Further Reading

- [Optional resource 1](URL)
- [Optional resource 2](URL)
```

---

### 3. Code Example

**Description**: Runnable Python script demonstrating a concept, with three complexity levels.

**Attributes**:
- `filename` (string): Python file name (e.g., "lesson-01-minimal.py")
- `lessonSlug` (string): Parent lesson
- `chapterNumber` (integer): Parent chapter
- `complexityLevel` (enum): "minimal", "working", "extended"
- `language` (string): "python" (fixed for this course)
- `pythonVersion` (string): Minimum Python version (e.g., "3.8+")
- `dependencies` (array of objects): Required packages with pinned versions
  - `name` (string): Package name (e.g., "pybullet")
  - `version` (string): Exact version (e.g., "3.2.5")
- `platformSupport` (array of enum): ["windows", "macos", "linux"]
- `lineCount` (integer): Approximate number of lines
- `description` (string): One-sentence explanation of what code demonstrates
- `hasComments` (boolean): Whether code includes inline comments
- `tested` (boolean): Whether code has been validated on all platforms

**Complexity Level Definitions**:
- **Minimal** (<10 lines): Core concept only, minimal setup/teardown
- **Working** (10-50 lines): Complete example with full setup, error handling, documentation
- **Extended** (50+ lines): Production-ready with comprehensive error handling, logging, modularity

**Relationships**:
- Belongs to: Lesson
- References: Dependencies (Python packages)

**Validation Rules**:
- Code MUST run without errors on Windows, macOS, and Linux
- Code MUST specify Python version requirement in header comment
- Code MUST include dependencies in chapter's `requirements.txt`
- Code MUST include inline comments explaining non-obvious logic
- Working and Extended examples MUST include error handling
- All examples MUST be tested before publication

**File Organization**:
```
static/code-examples/chapter-{##}/
├── requirements.txt
├── setup.sh
├── setup.bat
├── lesson-{##}-minimal.py
├── lesson-{##}-working.py
├── lesson-{##}-extended.py
└── utils.py (shared utilities)
```

**File Header Template**:
```python
"""
Lesson {chapter}.{lesson}: {concept}
Description: {description}

Requirements:
- Python 3.8+
- Dependencies: listed in requirements.txt

Usage:
    python lesson-{##}-{level}.py

Author: Physical AI Course Contributors
License: MIT
"""

# Import dependencies with version comments
import pybullet as p  # pybullet==3.2.5
import numpy as np     # numpy==1.21.0
```

---

### 4. Assessment

**Description**: Mechanism to verify student understanding through quizzes, reflection questions, or mini-projects.

**Attributes**:
- `lessonSlug` (string): Parent lesson
- `type` (enum): "quiz", "reflection", "mini-project", "mixed"
- `questions` (array of objects): Assessment items
  - `text` (string): Question or prompt
  - `type` (enum): "multiple-choice", "true-false", "short-answer", "coding-exercise"
  - `options` (array of strings): For multiple-choice (optional)
  - `correctAnswer` (string or array): Correct response(s) (optional, may be private)
  - `explanation` (string): Why answer is correct, learning reinforcement
- `successCriteria` (string): Clear statement of what constitutes passing/completion
- `estimatedMinutes` (integer): Expected time to complete assessment (5-20 minutes)

**Relationships**:
- Belongs to: Lesson (one-to-one)

**Validation Rules**:
- Every lesson MUST have exactly one assessment
- Assessment MUST include clear success criteria
- Multiple-choice questions MUST have 3-4 options
- Coding exercises MUST specify expected output or behavior

**Example Assessment Structure**:
```markdown
## Self-Assessment

**Success Criteria**: Answer at least 4 out of 5 questions correctly to demonstrate understanding.

### Question 1: Multiple Choice

What is the primary advantage of Physical AI over virtual AI?

A) Lower computational cost
B) Interaction with the physical world
C) Easier to implement
D) Faster training times

**Answer**: B

**Explanation**: Physical AI systems interact with and manipulate the real world, enabling applications like manufacturing, healthcare, and exploration that virtual AI cannot directly accomplish.

### Question 2: Reflection

Describe a scenario where physical AI could improve safety compared to human operation. Consider factors like repetition, hazardous environments, and precision.

**Success Criteria**: Response includes specific scenario, identifies safety advantages, and considers physical AI capabilities.

### Question 3: Mini-Project

Modify the "Hello Robot" simulation to make the robot move in a circle instead of a square. Test your code and observe the robot's path.

**Success Criteria**: Robot completes at least one full circular path in simulation without errors.
```

---

### 5. Visual Asset

**Description**: Diagram, image, or video supporting lesson content, with accessibility metadata.

**Attributes**:
- `filename` (string): File name (e.g., "figure-21-sensor-loop.svg")
- `chapterNumber` (integer): Parent chapter
- `lessonNumber` (integer or null): Parent lesson (null if chapter-level asset)
- `figureNumber` (string): Sequential numbering within chapter (e.g., "Figure 2.1")
- `type` (enum): "diagram", "photo", "screenshot", "video-embed"
- `format` (enum): "svg", "png", "jpg", "mp4", "youtube-embed"
- `altText` (string): Accessibility description for screen readers
- `caption` (string): Figure caption displayed below image
- `sourceFile` (string): Path to editable source (e.g., draw.io file)
- `resolution` (string): For raster images (e.g., "300 DPI")
- `license` (string): Usage rights (e.g., "CC-BY-4.0", "Original")

**Relationships**:
- Belongs to: Chapter or Lesson
- May have: Source File (editable .drawio, .py, etc.)

**Validation Rules**:
- Diagrams MUST be SVG (preferred) or PNG at 300 DPI minimum
- All assets MUST include alt text for accessibility
- Videos MUST include captions and timestamps
- Photos MUST be appropriately compressed for web (<500 KB)
- Source files SHOULD be stored for future editing

**File Organization**:
```
static/img/
├── sources/           # Editable source files
│   └── chapter-##/
│       ├── figure-##.drawio
│       └── plot-##.py
└── chapter-##/        # Published assets
    ├── figure-##-name.svg
    ├── photo-##-name.jpg
    └── diagram-##-name.png
```

**Usage in Markdown**:
```markdown
![Sensor feedback loop showing sensor→controller→actuator→system](../../../static/img/chapter-02/figure-21-sensor-loop.svg)

**Figure 2.1**: Sensor feedback loop demonstrating closed-loop control in a robotic system.
```

---

## Entity Relationships Diagram

```
Chapter (1)
├── has many (3) ──> Lesson
├── has one ──> Category Config File
└── has many ──> Visual Assets (chapter-level)

Lesson (1)
├── belongs to ──> Chapter
├── has many (0-5) ──> Code Examples
├── has many (0-10) ──> Visual Assets
├── has one ──> Assessment
└── references many ──> Prerequisites (Lessons)

Code Example (1)
├── belongs to ──> Lesson
└── references many ──> Dependencies

Assessment (1)
└── belongs to ──> Lesson

Visual Asset (1)
├── belongs to ──> Chapter OR Lesson
└── may have ──> Source File
```

## Data Integrity Constraints

1. **Chapter Completeness**: Every chapter MUST have exactly 3 lessons
2. **Lesson Structure**: Every lesson MUST include all 8 mandatory components
3. **Code Testability**: All code examples MUST pass validation tests
4. **Cross-References**: All prerequisite links MUST point to existing lessons
5. **Asset Accessibility**: All visual assets MUST include alt text
6. **Sequential Numbering**: Chapter/lesson numbers MUST be sequential and unique
7. **Safety Compliance**: Lessons with physical systems MUST include safety content

## File System Mapping

### Docusaurus Content Structure

```
docs/
├── index.md (Course home)
├── chapter-01-introduction/
│   ├── _category_.json (Chapter metadata)
│   ├── lesson-01-what-is-physical-ai.md (Lesson 1.1)
│   ├── lesson-02-safety-and-ethics.md (Lesson 1.2)
│   └── lesson-03-setup-environment.md (Lesson 1.3)
├── chapter-02-sensors/
│   └── ... (3 lessons)
└── ... (chapters 3-10)

static/
├── code-examples/
│   ├── chapter-01/
│   │   ├── requirements.txt
│   │   ├── setup.sh
│   │   ├── setup.bat
│   │   └── lesson-*-.py
│   └── ... (chapters 2-10)
└── img/
    ├── sources/ (editable draw.io, .py)
    ├── chapter-01/
    │   └── figure-*.svg
    └── ... (chapters 2-10)
```

## Data Flow

1. **Content Creation**:
   - Author writes Lesson Markdown → Validates against template → Commits to Git

2. **Code Development**:
   - Author writes Python code → Tests in venv → Adds to `code-examples/` → Validation script confirms

3. **Diagram Creation**:
   - Author creates diagram in draw.io → Exports SVG → Stores source and export → References in Markdown

4. **Build Process**:
   - Docusaurus reads `docs/` and `static/` → Generates static HTML → Deploys to hosting

5. **Student Experience**:
   - Student navigates via sidebar → Reads lesson → Downloads code examples → Runs locally → Completes assessment

## Schema Evolution

**Versioning Strategy**: Use Docusaurus versioning plugin for major course updates

- **v1.0**: Initial 10-chapter, 30-lesson course (defined in this spec)
- **v2.0** (future): Potential additions (e.g., advanced topics, new chapters)
- **Content updates**: Minor edits (typo fixes, clarifications) don't require versioning

**Backward Compatibility**: Ensure older lesson URLs remain valid when adding content
