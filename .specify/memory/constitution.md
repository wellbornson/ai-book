<!--
Sync Impact Report:
- Version: 0.0.0 → 1.0.0
- Modified principles: All (initial constitution creation)
- Added sections: All core sections
- Removed sections: None
- Templates requiring updates:
  ✅ plan-template.md (reviewed - compatible with new constitution)
  ✅ spec-template.md (reviewed - compatible with new constitution)
  ✅ tasks-template.md (reviewed - compatible with new constitution)
- Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Course Constitution

## Core Principles

### I. Accessibility-First Learning

Every concept MUST be introduced with clear, jargon-free explanations before technical depth. Content MUST progress from beginner-friendly overviews to intermediate technical details. Complex topics MUST include visual aids (diagrams, images, videos) and real-world analogies to bridge understanding gaps.

**Rationale**: The target audience spans beginners to intermediate learners. Starting with accessible language ensures no learner is left behind, while progressive depth satisfies more advanced students. Visual learning aids accommodate different learning styles and improve retention.

### II. Hands-On Practice Mandatory

Every theoretical concept MUST be accompanied by at least one practical exercise, lab, or project. Code examples MUST be runnable, complete, and thoroughly commented. Projects MUST build progressively, with each chapter adding new capabilities to previous work.

**Rationale**: Physical AI and robotics cannot be learned through reading alone. Hands-on practice solidifies understanding, builds confidence, and prepares students for real-world applications. Progressive projects create a sense of accomplishment and demonstrate how concepts connect.

### III. Safety and Ethics Non-Negotiable

Every section involving physical systems, actuators, or autonomous behavior MUST include explicit safety warnings and precautions. Ethical considerations (privacy, bias, safety, societal impact) MUST be addressed for AI and robotics applications. All code examples MUST implement appropriate fail-safes and error handling.

**Rationale**: Physical AI and humanoid robotics can cause harm if improperly implemented. Students must develop safety-conscious habits from day one. Ethical awareness prepares students to build responsible AI systems that consider human welfare and societal impact.

### IV. Docusaurus-Native Content Structure

All content MUST be structured as Markdown files compatible with Docusaurus documentation framework. Navigation MUST follow Docusaurus sidebar conventions with logical chapter/section hierarchies. Interactive elements (code blocks, tabs, admonitions) MUST use Docusaurus components and syntax.

**Rationale**: Docusaurus provides a modern, searchable, mobile-responsive documentation platform. Adhering to its conventions ensures maintainability, enables versioning, and provides excellent developer experience. Native components enhance interactivity without custom development.

### V. Curriculum Completeness and Coherence

Content MUST cover the full spectrum from foundations (sensors, actuators, kinematics) through advanced topics (perception, manipulation, learning). Each chapter MUST explicitly state prerequisites and learning objectives. Cross-references MUST be provided when topics relate to other sections, with clear links.

**Rationale**: A complete curriculum ensures students can progress from zero knowledge to intermediate proficiency. Explicit prerequisites allow students to self-assess readiness. Cross-references help students see connections and build a mental model of how concepts integrate.

### VI. Code Quality and Reproducibility

All code examples MUST include version numbers for dependencies and frameworks. Environment setup instructions MUST be complete and tested on target platforms (Windows, macOS, Linux). Code MUST follow language-specific best practices with clear inline comments explaining non-obvious logic.

**Rationale**: Reproducibility is essential for learners working independently. Incomplete setup instructions or version mismatches cause frustration and impede learning. Clear, well-commented code serves as both tutorial and reference material.

### VII. Active Learning and Assessment

Each chapter MUST include self-assessment questions or quizzes to verify understanding. Projects MUST include clear success criteria so students know when they've completed objectives. Challenge exercises MUST be provided for advanced students seeking deeper exploration.

**Rationale**: Active recall through quizzes improves long-term retention. Clear success criteria reduce ambiguity and build student confidence. Challenge exercises provide depth without overwhelming beginners, catering to diverse skill levels.

## Content Standards

### Chapter Structure (Mandatory)

Every chapter MUST include:

1. **Learning Objectives** (3-5 bullet points describing what students will learn)
2. **Prerequisites** (list of prior chapters or concepts required)
3. **Theory Section** (conceptual explanation with visuals)
4. **Practical Section** (hands-on exercises with step-by-step instructions)
5. **Code Examples** (complete, runnable, commented)
6. **Safety Considerations** (where applicable)
7. **Self-Assessment** (quiz, reflection questions, or mini-project)
8. **Further Reading** (optional resources for deeper exploration)

### Technical Stack and Tools

The course MUST use the following technologies:

- **Documentation Platform**: Docusaurus (latest stable version)
- **Primary Programming Language**: Python 3.8+ (for accessibility and ecosystem support)
- **Simulation Environment**: Recommend PyBullet, Gazebo, or similar (with clear setup guides)
- **Hardware Recommendations**: Raspberry Pi, Arduino, or equivalent accessible platforms
- **Version Control**: All code examples MUST be compatible with Git workflows

### Multimedia and Interactivity

- **Diagrams**: MUST be vector-based (SVG preferred) or high-resolution raster (PNG 300 DPI minimum)
- **Videos**: MUST include timestamps and closed captions for accessibility
- **Code Playgrounds**: Leverage Docusaurus live code blocks where practical
- **3D Visualizations**: Recommend Three.js or similar web-based viewers when demonstrating spatial concepts

## Development Workflow

### Content Creation Process

1. **Outline Stage**: Define chapter learning objectives and prerequisite knowledge
2. **Draft Stage**: Write theory with placeholders for visuals and code
3. **Code Development**: Create and test all code examples in isolated environments
4. **Integration**: Embed code and create supporting visuals
5. **Review**: Technical accuracy review and peer feedback
6. **Testing**: Have a beginner-level tester follow the chapter independently
7. **Refinement**: Address tester feedback and clarify confusing sections

### Quality Gates

Before publishing any chapter:

- [ ] All code examples run without errors
- [ ] Prerequisites are explicitly stated
- [ ] Safety warnings are present where needed
- [ ] At least one practical exercise is included
- [ ] Self-assessment mechanism is present
- [ ] Content is free of jargon without definitions
- [ ] Visuals support key concepts
- [ ] Docusaurus build succeeds without warnings

### Review and Revision

- **Peer Review**: Every chapter MUST be reviewed by at least one other contributor for technical accuracy
- **Student Testing**: Chapters MUST be tested by at least one person matching the target audience (beginner-intermediate)
- **Feedback Loop**: Student feedback MUST be collected and incorporated within one revision cycle
- **Version History**: Significant content changes MUST be documented in chapter changelog

## Governance

### Amendment Process

This constitution supersedes all other project practices and style guides. Amendments require:

1. Documentation of the proposed change with rationale
2. Review by core contributors or course maintainers
3. Migration plan for affected content (if applicable)
4. Version increment per semantic versioning rules
5. Update of all dependent templates and documentation

### Compliance Verification

All contributions (pull requests, new chapters, exercises) MUST be verified for compliance with:

- Accessibility and safety principles
- Docusaurus structure and conventions
- Code quality and reproducibility standards
- Chapter structure requirements

Non-compliant contributions MUST be flagged with specific principle violations before acceptance.

### Version Control and Change Management

- **Breaking Changes** (MAJOR version): Fundamental restructuring, principle removal, tech stack changes
- **Feature Additions** (MINOR version): New principles, expanded guidelines, new sections
- **Clarifications** (PATCH version): Wording improvements, typo fixes, non-semantic refinements

All changes MUST be reflected in dependent template files within the same commit cycle.

### Complexity Justification

Any practice that adds complexity beyond core principles MUST be explicitly justified. Examples requiring justification:

- Custom Docusaurus plugins (vs built-in features)
- Additional programming languages (vs Python-only)
- Advanced prerequisite topics (vs beginner-intermediate focus)
- Non-standard tooling (vs recommended stack)

Justifications MUST explain the benefit, document why simpler alternatives are insufficient, and provide migration paths if the complex solution is later simplified.

---

**Version**: 1.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06
