# Tasks: Physical AI Book Structure

**Input**: Design documents from `/specs/001-book-structure/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: No explicit test tasks included (documentation project - validation via build success and quality gates)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

This is a Docusaurus documentation project with the following structure:
- **Core configuration**: `docusaurus.config.js`, `sidebars.js` at repository root
- **Content**: `docs/` directory containing Markdown files
- **Static assets**: `static/img/` (images), `static/code-examples/` (Python code)
- **Scripts**: `scripts/` for validation and build automation

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize Docusaurus project with base configuration and directory structure

- [ ] T001 Initialize Docusaurus project using `npx create-docusaurus@latest docs classic` in repository root
- [ ] T002 Install Node.js dependencies with `npm install` in docs/ directory
- [ ] T003 [P] Create `.gitignore` file in repository root with entries for `node_modules/`, `build/`, `.docusaurus/`, `__pycache__/`, `venv/`
- [ ] T004 [P] Update `docusaurus.config.js` with course metadata (title, tagline, URL, organization, GitHub link)
- [ ] T005 [P] Configure Prism syntax highlighting for Python and Bash in `docusaurus.config.js` themeConfig.prism
- [ ] T006 [P] Create custom CSS file at `docs/src/css/custom.css` with course branding colors (if needed)
- [ ] T007 Create directory structure for 10 chapters: `docs/chapter-01-introduction/` through `docs/chapter-10-integration/`
- [ ] T008 [P] Create directory structure for static assets: `static/img/chapter-01/` through `static/img/chapter-10/` and `static/img/sources/`
- [ ] T009 [P] Create directory structure for code examples: `static/code-examples/chapter-01/` through `static/code-examples/chapter-10/`
- [ ] T010 [P] Create scripts directory with placeholder files: `scripts/validate-code-examples.py`, `scripts/check-links.js`, `scripts/lint-markdown.sh`
- [ ] T011 Test local development server with `npm start` - verify site loads at localhost:3000
- [ ] T012 Test production build with `npm run build` - verify build succeeds without errors

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core configuration and templates that MUST be complete before content development

**⚠️ CRITICAL**: No chapter content work can begin until this phase is complete

- [ ] T013 Configure `sidebars.js` with complete 10-chapter structure (10 categories with 3 docs each placeholder)
- [ ] T014 [P] Create `_category_.json` file in `docs/chapter-01-introduction/` with metadata: label "Chapter 1: Introduction", position 1, description
- [ ] T015 [P] Create `_category_.json` file in `docs/chapter-02-sensors/` with metadata: label "Chapter 2: Sensors", position 2, description
- [ ] T016 [P] Create `_category_.json` file in `docs/chapter-03-actuators/` with metadata
- [ ] T017 [P] Create `_category_.json` file in `docs/chapter-04-kinematics/` with metadata
- [ ] T018 [P] Create `_category_.json` file in `docs/chapter-05-control/` with metadata
- [ ] T019 [P] Create `_category_.json` file in `docs/chapter-06-path-planning/` with metadata
- [ ] T020 [P] Create `_category_.json` file in `docs/chapter-07-machine-learning/` with metadata
- [ ] T021 [P] Create `_category_.json` file in `docs/chapter-08-manipulation/` with metadata
- [ ] T022 [P] Create `_category_.json` file in `docs/chapter-09-humanoid/` with metadata
- [ ] T023 [P] Create `_category_.json` file in `docs/chapter-10-integration/` with metadata
- [ ] T024 Create course home page at `docs/index.md` with overview, learning path, prerequisites, navigation guidance
- [ ] T025 Create validation script `scripts/validate-code-examples.py` that tests all Python code runs without errors
- [ ] T026 [P] Create link checker script `scripts/check-links.js` that verifies all internal Markdown links are valid
- [ ] T027 [P] Create Markdown linter script `scripts/lint-markdown.sh` using markdownlint
- [ ] T028 Test build with foundational structure - verify sidebar displays all 10 chapters and home page renders

**Checkpoint**: Foundation ready - chapter content development can now begin in parallel

---

## Phase 3: User Story 1 - Navigate Course Structure (Priority: P1) 🎯 MVP

**Goal**: Students can navigate through chapters and lessons systematically using Docusaurus sidebar

**Independent Test**: Open site at localhost:3000, verify sidebar displays all chapters and lessons with correct hierarchy, click any lesson to confirm it loads, verify breadcrumbs show current location

### Scaffolding for User Story 1

- [ ] T029 [P] [US1] Create empty lesson file `docs/chapter-01-introduction/lesson-01-what-is-physical-ai.md` with front matter (title, sidebar_position: 1, description, tags)
- [ ] T030 [P] [US1] Create empty lesson file `docs/chapter-01-introduction/lesson-02-safety-and-ethics.md` with front matter (title, sidebar_position: 2, description, tags)
- [ ] T031 [P] [US1] Create empty lesson file `docs/chapter-01-introduction/lesson-03-setup-environment.md` with front matter (title, sidebar_position: 3, description, tags)
- [ ] T032 [P] [US1] Create empty lesson file `docs/chapter-02-sensors/lesson-01-sensor-fundamentals.md` with front matter
- [ ] T033 [P] [US1] Create empty lesson file `docs/chapter-02-sensors/lesson-02-vision-sensors.md` with front matter
- [ ] T034 [P] [US1] Create empty lesson file `docs/chapter-02-sensors/lesson-03-lidar-depth-multimodal.md` with front matter
- [ ] T035 [P] [US1] Create empty lesson file `docs/chapter-03-actuators/lesson-01-actuator-types.md` with front matter
- [ ] T036 [P] [US1] Create empty lesson file `docs/chapter-03-actuators/lesson-02-motor-control-pwm.md` with front matter
- [ ] T037 [P] [US1] Create empty lesson file `docs/chapter-03-actuators/lesson-03-programming-movements.md` with front matter
- [ ] T038 [P] [US1] Create empty lesson files for remaining 21 lessons (chapters 4-10, 3 lessons each) with front matter
- [ ] T039 [US1] Update `sidebars.js` with all 30 lesson document IDs in correct chapter categories
- [ ] T040 [US1] Test navigation: verify sidebar displays all 10 chapters with 3 lessons each, clicking lessons loads pages
- [ ] T041 [US1] Verify breadcrumbs display correctly on lesson pages showing "Chapter > Lesson" hierarchy
- [ ] T042 [US1] Test previous/next navigation buttons work correctly between sequential lessons

**Checkpoint**: At this point, User Story 1 (Navigation) is fully functional - students can navigate through all course structure

---

## Phase 4: User Story 2 - Complete Structured Learning Content (Priority: P1)

**Goal**: Each lesson follows consistent 8-component format with learning objectives, theory, practice, code, safety, assessment

**Independent Test**: Open any lesson, scroll through content, verify all 8 mandatory components are present in prescribed order

**Note**: This phase demonstrates implementation for Chapter 1 (3 lessons). Repeat pattern for remaining chapters.

### Chapter 1 Content Development

#### Lesson 1.1: What is Physical AI?

- [ ] T043 [P] [US2] Write Learning Objectives section (3-5 bullet points) in `docs/chapter-01-introduction/lesson-01-what-is-physical-ai.md`
- [ ] T044 [P] [US2] Write Prerequisites section (this is first lesson, state no prerequisites required)
- [ ] T045 [US2] Write Theory section with jargon-free introduction, define Physical AI, explain perception-cognition-action loop
- [ ] T046 [US2] Create diagram `static/img/chapter-01/figure-11-physical-ai-loop.svg` showing perception-cognition-action cycle using draw.io
- [ ] T047 [US2] Write comparison table of Physical AI vs Virtual AI in Theory section
- [ ] T048 [US2] Write real-world applications subsection (manufacturing, healthcare, exploration, everyday life)
- [ ] T049 [US2] Write Hands-On Practice section with exercise to watch robot videos and identify sensors/actuators/tasks
- [ ] T050 [US2] Write Code Examples section (no actual code for this conceptual lesson, provide preview of what's coming in Lesson 1.3)
- [ ] T051 [US2] Write Self-Assessment section with 4 questions (multiple choice, true/false, short answer, application analysis)
- [ ] T052 [US2] Write Further Reading section with links to articles, videos, academic resources
- [ ] T053 [US2] Add lesson summary section restating learning objectives and key concepts
- [ ] T054 [US2] Review Lesson 1.1 against constitution quality gates checklist (jargon-free, visuals, prerequisites stated, exercise included, assessment present)

#### Lesson 1.2: Safety and Ethics in Robotics

- [ ] T055 [P] [US2] Write Learning Objectives section (3-5 bullet points about safety principles, hazard identification, ethical considerations)
- [ ] T056 [P] [US2] Write Prerequisites section (link to Lesson 1.1)
- [ ] T057 [US2] Write Theory section introducing safety-first principles for physical systems
- [ ] T058 [US2] Create diagram `static/img/chapter-01/figure-12-safety-workflow.svg` showing hazard identification → risk assessment → mitigation → testing workflow
- [ ] T059 [US2] Write hazard identification subsection (mechanical, electrical, software, environmental hazards)
- [ ] T060 [US2] Write risk assessment subsection (likelihood, severity, risk matrix)
- [ ] T061 [US2] Write fail-safe design subsection (emergency stops, redundancy, fault detection)
- [ ] T062 [US2] Write ethical considerations subsection (privacy in surveillance robots, bias in AI, job displacement, responsible innovation)
- [ ] T063 [US2] Write Hands-On Practice section with exercise to analyze robot scenarios for safety risks and ethical concerns
- [ ] T064 [US2] Write Code Examples section (conceptual lesson, explain how code will include safety checks in future lessons)
- [ ] T065 [US2] Write Safety Considerations section (meta - this lesson IS about safety, discuss developing safety-conscious habits)
- [ ] T066 [US2] Write Self-Assessment section with questions on hazard identification, ethical scenarios, risk mitigation strategies
- [ ] T067 [US2] Write Further Reading section (safety standards, ethics papers, case studies)
- [ ] T068 [US2] Review Lesson 1.2 against constitution quality gates checklist

#### Lesson 1.3: Setting Up Your Development Environment

- [ ] T069 [P] [US2] Write Learning Objectives section (install Python, PyBullet, run first simulation)
- [ ] T070 [P] [US2] Write Prerequisites section (link to Lessons 1.1 and 1.2)
- [ ] T071 [US2] Write Theory section explaining development environment components (Python, virtual environments, PyBullet, version control)
- [ ] T072 [US2] Create diagram `static/img/chapter-01/figure-13-dev-environment.svg` showing relationship between Python, venv, PyBullet, IDE
- [ ] T073 [US2] Write Hands-On Practice section with step-by-step Python installation instructions for Windows, macOS, Linux
- [ ] T074 [US2] Write virtual environment setup instructions (python -m venv, activation commands for all platforms)
- [ ] T075 [US2] Write PyBullet installation instructions (pip install pybullet)
- [ ] T076 [P] [US2] Create `static/code-examples/chapter-01/requirements.txt` with pybullet==3.2.5 and other dependencies
- [ ] T077 [P] [US2] Create `static/code-examples/chapter-01/setup.sh` script for Linux/macOS virtual environment setup
- [ ] T078 [P] [US2] Create `static/code-examples/chapter-01/setup.bat` script for Windows virtual environment setup
- [ ] T079 [US2] Write minimal code example `static/code-examples/chapter-01/lesson-03-minimal.py` (<10 lines): connect to PyBullet, set gravity, disconnect
- [ ] T080 [US2] Write working code example `static/code-examples/chapter-01/lesson-03-working.py` (10-50 lines): complete "Hello Robot" simulation with sphere creation and physics step
- [ ] T081 [US2] Write extended code example `static/code-examples/chapter-01/lesson-03-extended.py` (50+ lines): production-ready with error handling, logging, context manager
- [ ] T082 [US2] Test all code examples on Windows - verify they run without errors
- [ ] T083 [US2] Test all code examples on macOS - verify they run without errors
- [ ] T084 [US2] Test all code examples on Linux - verify they run without errors
- [ ] T085 [US2] Write Code Examples section in lesson with inline explanations of minimal, working, extended examples
- [ ] T086 [US2] Write Safety Considerations section (if working with physical hardware in future, emphasize testing in simulation first)
- [ ] T087 [US2] Write Self-Assessment section with questions on installation steps, virtual environments, running first simulation
- [ ] T088 [US2] Write Further Reading section (Python docs, PyBullet tutorials, virtual environment best practices)
- [ ] T089 [US2] Review Lesson 1.3 against constitution quality gates checklist

### Chapter 1 Integration and Review

- [ ] T090 [US2] Create chapter overview content for `docs/chapter-01-introduction/_category_.json` generated index page
- [ ] T091 [US2] Add cross-references between lessons (e.g., Lesson 1.3 references safety from 1.2)
- [ ] T092 [US2] Verify all images display correctly in all 3 lessons
- [ ] T093 [US2] Verify all code examples are linked and downloadable
- [ ] T094 [US2] Run validation script `scripts/validate-code-examples.py` on Chapter 1 code - ensure all pass
- [ ] T095 [US2] Run link checker `scripts/check-links.js` on Chapter 1 - ensure no broken links
- [ ] T096 [US2] Run Markdown linter `scripts/lint-markdown.sh` on Chapter 1 - fix any formatting issues
- [ ] T097 [US2] Build site with `npm run build` - verify Chapter 1 builds without warnings
- [ ] T098 [US2] Manual review of Chapter 1 by peer reviewer for technical accuracy and clarity
- [ ] T099 [US2] Student testing: have 2-3 beginner-level testers complete Chapter 1 independently, collect feedback
- [ ] T100 [US2] Incorporate peer review and student feedback into Chapter 1 lessons
- [ ] T101 [US2] Final quality check: verify all 3 lessons pass constitution quality gates (code runs, prerequisites stated, safety present, exercises included, assessment present, jargon-free, visuals present, build succeeds)

**Checkpoint**: At this point, User Story 2 is validated with Chapter 1 as proof - all 3 lessons follow 8-component format and pass quality gates. This template is ready to replicate for chapters 2-10.

---

## Phase 5: User Story 3 - Access Safe and Ethical Learning Content (Priority: P2)

**Goal**: Lessons involving physical systems include explicit safety warnings and ethical considerations

**Independent Test**: Review Chapter 3 (Actuators) lessons and verify safety warnings are present, review Chapter 7 (ML) lessons and verify ethical considerations addressed

**Note**: This user story is validated by constitution compliance in Phase 4 (Chapter 1 Lesson 1.2 dedicated to safety/ethics, Lesson 1.3 includes safety section). Additional validation occurs during development of chapters involving physical systems.

### Validation Tasks for User Story 3

- [ ] T102 [US3] Review lesson template `specs/001-book-structure/contracts/lesson-template.md` to confirm Safety Considerations section is included (conditional on content type)
- [ ] T103 [US3] Create safety warnings template with standard phrasing for common hazards (motor control, high voltage, mechanical pinch points, etc.)
- [ ] T104 [US3] Create ethics considerations template for AI decision-making topics (bias, privacy, transparency, accountability)
- [ ] T105 [US3] Verify Chapter 1 Lesson 1.2 (Safety and Ethics) is complete and serves as reference for other chapters
- [ ] T106 [US3] When developing Chapter 3 (Actuators), ensure all 3 lessons include Safety Considerations sections with specific warnings for motors, torque, emergency stops
- [ ] T107 [US3] When developing Chapter 7 (ML), ensure ethical considerations are addressed in lessons on RL, imitation learning, and decision-making
- [ ] T108 [US3] When developing Chapter 9 (Humanoid), ensure HRI lesson includes physical safety and social ethics content
- [ ] T109 [US3] Run content audit after all chapters complete: verify 100% of lessons with physical systems include safety content, verify ethics addressed where applicable

**Checkpoint**: User Story 3 requirements are met through template enforcement and content review process

---

## Phase 6: User Story 4 - Search and Reference Content (Priority: P3)

**Goal**: Students can search across course content and use cross-references to find related concepts

**Independent Test**: Use search bar to find specific terms, verify results appear from multiple chapters, click cross-reference links and confirm they navigate to correct sections

### Search and Navigation Enhancement

- [ ] T110 [US4] Research Algolia DocSearch setup for open-source projects (free tier) or use built-in Docusaurus search
- [ ] T111 [US4] If using Algolia: Sign up for DocSearch, obtain API key and app ID
- [ ] T112 [US4] Configure search in `docusaurus.config.js` themeConfig.algolia (or enable built-in search)
- [ ] T113 [US4] Test search functionality: search for "sensor", "actuator", "safety" - verify results appear from multiple chapters
- [ ] T114 [US4] Add keywords to front matter of high-traffic lessons to improve search relevance
- [ ] T115 [P] [US4] Review all lessons and add cross-reference links where concepts relate to other sections (e.g., "See Lesson 4.1 for forward kinematics")
- [ ] T116 [P] [US4] Create glossary page `docs/glossary.md` with definitions of key terms linked from lessons
- [ ] T117 [US4] Add "Related Lessons" sections to lessons that build on each other (e.g., PID control lesson references motor control lesson)
- [ ] T118 [US4] Test all cross-reference links with `scripts/check-links.js` - verify no broken internal links
- [ ] T119 [US4] Create course roadmap visualization showing prerequisite relationships between chapters
- [ ] T120 [US4] Add roadmap to home page `docs/index.md` to help students plan learning path
- [ ] T121 [US4] Test search performance: measure time to return results for common queries (target <2 seconds per SC-007)
- [ ] T122 [US4] User testing: have students find specific topics using search and navigation, measure time (target <1 minute per SC-008)

**Checkpoint**: User Story 4 is complete - search returns relevant results quickly, cross-references enable easy navigation between related concepts

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple chapters and final production readiness

- [ ] T123 [P] Update README.md in repository root with project description, setup instructions, contribution guidelines
- [ ] T124 [P] Create CONTRIBUTING.md with guidelines for adding/updating content, lesson template usage, code standards
- [ ] T125 [P] Create LICENSE file with appropriate open-source license (MIT, CC-BY-4.0, or as determined)
- [ ] T126 [P] Add favicon at `static/img/favicon.ico`
- [ ] T127 [P] Add course logo at `static/img/logo.svg` and update navbar logo in `docusaurus.config.js`
- [ ] T128 [P] Create social media preview image `static/img/social-card.png` (1200x630px) and configure in docusaurus.config.js
- [ ] T129 [P] Configure footer in `docusaurus.config.js` with copyright, links to GitHub, about page, contact
- [ ] T130 [P] Create About page `docs/about.md` with course background, contributors, acknowledgments
- [ ] T131 Perform full site build with `npm run build` - verify no warnings or errors
- [ ] T132 Run accessibility audit using Lighthouse - target score >90, fix any critical issues
- [ ] T133 Test site responsiveness on mobile devices (iOS Safari, Android Chrome) - verify navigation and content render correctly
- [ ] T134 Test site on different browsers (Chrome, Firefox, Safari, Edge) - ensure compatibility
- [ ] T135 Run all validation scripts (`validate-code-examples.py`, `check-links.js`, `lint-markdown.sh`) on entire site - fix any remaining issues
- [ ] T136 Create deployment configuration for hosting platform (GitHub Pages, Netlify, or Vercel)
- [ ] T137 Set up continuous deployment (CD) pipeline to auto-deploy on commits to main branch (optional but recommended)
- [ ] T138 Deploy production site to hosting platform
- [ ] T139 Verify deployed site matches local build - check all pages load, search works, images display
- [ ] T140 Set up analytics (Google Analytics, Plausible, or similar) to track page views and user engagement (optional)
- [ ] T141 Create issue templates in GitHub repository for bug reports, content suggestions, general questions
- [ ] T142 Set up GitHub Projects board for tracking content updates and community contributions
- [ ] T143 Document maintenance schedule (annual content review, dependency updates) in repository wiki or docs
- [ ] T144 Create student feedback collection mechanism (Google Form, Typeform, or embedded survey)
- [ ] T145 Final end-to-end test: have complete beginner follow course from start, collect comprehensive feedback

**Checkpoint**: Course is fully polished, deployed, and ready for students with maintainability processes in place

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) completion - BLOCKS all user story work
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) - navigation scaffolding
- **User Story 2 (Phase 4)**: Depends on US1 (Phase 3) - content added to navigable structure
- **User Story 3 (Phase 5)**: Validation occurs during US2 (Phase 4) - no hard dependency, can verify in parallel
- **User Story 4 (Phase 6)**: Depends on US2 (Phase 4) having substantial content - search needs content to index
- **Polish (Phase 7)**: Depends on all user stories (Phases 3-6) being substantially complete

### User Story Dependencies

- **User Story 1 (Navigation)**: Foundation only - no other story dependencies
- **User Story 2 (Structured Content)**: Requires US1 navigation structure to exist
- **User Story 3 (Safety/Ethics)**: Validated within US2 content - no separate dependency
- **User Story 4 (Search/References)**: Requires US2 content to search and reference

### Task Dependencies Within Phases

**Setup (Phase 1)**:
- T001 (init Docusaurus) → T002 (npm install) → T011-T012 (test)
- T003-T010 can run in parallel after T001

**Foundational (Phase 2)**:
- T013 (sidebars.js) must complete before T028 (test)
- T014-T023 (category configs) can run in parallel
- T024 (home page) can be parallel with category configs
- T025-T027 (scripts) can run in parallel

**User Story 1 (Phase 3)**:
- T029-T038 (create lesson files) can ALL run in parallel
- T039 (update sidebars) depends on T029-T038 completion
- T040-T042 (test navigation) depend on T039

**User Story 2 (Phase 4)**:
- Within each lesson, tasks are mostly sequential (objectives → theory → practice → code → assessment)
- Parallel opportunities: T043-T044, T055-T056, T069-T070 (different lessons, objectives/prerequisites)
- Parallel opportunities: T046, T058, T072 (diagrams for different lessons)
- Parallel opportunities: T076-T078 (code setup files)
- Parallel opportunities: T082-T084 (testing on different platforms)
- Review/feedback tasks (T098-T100) must be sequential at end

**User Story 3 (Phase 5)**:
- T102-T104 (templates) can run in parallel
- T105-T109 are validation checkpoints, not blocking tasks

**User Story 4 (Phase 6)**:
- T110-T112 (search setup) sequential
- T115-T117 (content enhancements) can run in parallel
- T118-T122 (testing) sequential after content work

**Polish (Phase 7)**:
- T123-T130 (documentation/branding) can ALL run in parallel
- T131-T145 (testing/deployment) mostly sequential

### Parallel Opportunities

**Maximum Parallelization Example - Setup Phase**:
```
Launch in parallel after T001-T002:
- T003 (.gitignore)
- T004 (docusaurus.config.js metadata)
- T005 (Prism config)
- T006 (custom CSS)
- T007 (chapter directories)
- T008 (image directories)
- T009 (code example directories)
- T010 (script placeholders)
```

**Maximum Parallelization Example - Foundational Phase**:
```
Launch in parallel after T013:
- T014-T023 (all 10 _category_.json files)
- T024 (home page)
- T025-T027 (all validation scripts)
```

**Maximum Parallelization Example - US1 Navigation**:
```
Launch in parallel:
- T029-T038 and T038 continuation (all 30 lesson scaffold files)
```

**Maximum Parallelization Example - US2 Content (within lesson constraints)**:
```
For different lessons in parallel:
- T043-T044 (Lesson 1.1 objectives/prereqs)
- T055-T056 (Lesson 1.2 objectives/prereqs)
- T069-T070 (Lesson 1.3 objectives/prereqs)

For diagrams in parallel:
- T046 (Figure 1.1)
- T058 (Figure 1.2)
- T072 (Figure 1.3)

For code setup in parallel:
- T076 (requirements.txt)
- T077 (setup.sh)
- T078 (setup.bat)

For code examples in parallel:
- T079 (minimal)
- T080 (working)
- T081 (extended)
```

---

## Implementation Strategy

### MVP First (User Story 1 + Partial US2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Navigation scaffolding for all 30 lessons)
4. Complete Phase 4: User Story 2 for **Chapter 1 only** (3 fully developed lessons)
5. **STOP and VALIDATE**: Test Chapter 1 independently, verify navigation works, all components present
6. Deploy pilot site with Chapter 1 for early feedback
7. Use learnings to refine template before developing chapters 2-10

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add Navigation (US1) → All lesson pages exist (empty but navigable)
3. Develop Chapter 1 (US2) → Test independently → Deploy pilot (MVP!)
4. Develop Chapter 2 (US2) → Test independently → Deploy update
5. Develop Chapters 3-5 (US2) → Test each → Deploy (Core foundations complete)
6. Develop Chapters 6-10 (US2) → Test each → Deploy (Advanced topics complete)
7. Add Search (US4) → Deploy (Full feature set)
8. Polish (Phase 7) → Final production deployment

### Parallel Team Strategy

With multiple contributors:

1. Team completes Setup + Foundational together
2. Team member A: Creates navigation scaffolding (US1)
3. Once navigation ready:
   - Member B: Develops Chapter 1 (pilot)
   - Member C: Creates validation scripts
   - Member D: Sets up search and cross-references
4. After Chapter 1 validated:
   - Members work on different chapters in parallel (Chapters 2-10)
   - Each chapter independently developed, reviewed, tested
5. Team converges for Polish phase (deployment, final testing)

---

## Notes

- **[P] tasks** = different files, no dependencies on incomplete work, safe to run in parallel
- **[Story] labels** map tasks to user stories for traceability and independent testing
- Each user story phase should be independently completable and testable
- Verify Docusaurus build succeeds (`npm run build`) after each major phase
- Run validation scripts frequently to catch issues early
- Commit after each task or logical group for easy rollback if needed
- Stop at any checkpoint to validate user story independently before proceeding
- **Focus on Chapter 1 first as pilot** - validate template before scaling to 10 chapters
- Actual implementation effort: Chapter 1 pilot will reveal if 20-35 hour estimate per chapter from plan.md is accurate

---

## Task Summary

- **Total Tasks**: 145
- **Setup Phase**: 12 tasks (T001-T012)
- **Foundational Phase**: 16 tasks (T013-T028)
- **User Story 1** (Navigation): 14 tasks (T029-T042)
- **User Story 2** (Structured Content - Chapter 1): 59 tasks (T043-T101)
- **User Story 3** (Safety/Ethics): 8 tasks (T102-T109)
- **User Story 4** (Search/References): 13 tasks (T110-T122)
- **Polish Phase**: 23 tasks (T123-T145)

**Parallel Opportunities**: ~60 tasks marked with [P] can run in parallel within their phase constraints

**MVP Scope** (User Story 1 + Chapter 1 of US2): 87 tasks (T001-T042 + T043-T101)

**Format Validation**: ✅ All 145 tasks follow required checklist format with checkbox, Task ID, optional [P]/[Story] markers, description with file paths
