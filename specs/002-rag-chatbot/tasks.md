---

description: "Task list for RAG Chatbot for Published Book"
---

# Tasks: RAG Chatbot for Published Book

**Input**: Design documents from `/specs/002-rag-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan with backend directory
- [X] T002 Initialize Python 3.11 project with FastAPI, LangChain, Cohere, Qdrant-client, SQLAlchemy/asyncpg, Pydantic dependencies
- [X] T003 [P] Configure linting and formatting tools (black, flake8, mypy)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Setup database schema and migrations framework for Neon Postgres
- [X] T005 [P] Configure settings and environment management in backend/src/config/settings.py
- [X] T006 [P] Setup database connection and session management in backend/src/config/database.py
- [X] T007 Create base models/entities that all stories depend on (ChatSession, BookContent, UserQuery, RetrievedContext, GeneratedResponse)
- [X] T008 Configure error handling and logging infrastructure
- [X] T009 Setup authentication/authorization framework
- [X] T010 Configure Cohere API client with proper input_type specification
- [X] T011 Setup Qdrant vector database client and collection configuration
- [X] T012 Create ingestion service to handle PDF and text format processing
- [X] T013 Implement embedding service using Cohere embed-english-v3.0 with proper input_type for documents and queries

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Full Book Query (Priority: P1) 🎯 MVP

**Goal**: Enable users to ask questions about the entire book content and receive accurate, cited answers

**Independent Test**: The system can accept a user query about the book content and return an accurate response with proper citations to the relevant book sections within 2 seconds.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T014 [P] [US1] Contract test for POST /query endpoint in backend/tests/contract/test_query_api.py
- [X] T015 [P] [US1] Integration test for full book query flow in backend/tests/integration/test_full_book_query.py

### Implementation for User Story 1

- [X] T016 [P] [US1] Create BookContent model in backend/src/models/book_content.py
- [X] T017 [P] [US1] Create UserQuery model in backend/src/models/user_query.py
- [X] T018 [P] [US1] Create RetrievedContext model in backend/src/models/retrieved_context.py
- [X] T019 [P] [US1] Create GeneratedResponse model in backend/src/models/generated_response.py
- [X] T020 [US1] Implement retrieval service in backend/src/services/retrieval_service.py (depends on T013)
- [X] T021 [US1] Implement generation service in backend/src/services/generation_service.py (uses Cohere Command R/R+)
- [X] T022 [US1] Implement RAG service in backend/src/services/rag_service.py (integrates retrieval and generation)
- [X] T023 [US1] Implement query endpoint in backend/src/api/query_routes.py
- [X] T024 [US1] Add validation and error handling for full book queries
- [X] T025 [US1] Add logging for user story 1 operations
- [X] T026 [US1] Add performance monitoring to ensure <2s response times

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User-Selected Text Query (Priority: P2)

**Goal**: Allow users to select specific text from the book and ask questions only about that selected text

**Independent Test**: The system can accept user-selected text and respond to queries specifically about that text, ignoring the broader book context.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T027 [P] [US2] Contract test for POST /sessions/{session_id}/select-text endpoint in backend/tests/contract/test_text_selection_api.py
- [X] T028 [P] [US2] Integration test for user-selected text query flow in backend/tests/integration/test_selected_text_query.py

### Implementation for User Story 2

- [X] T029 [P] [US2] Update UserQuery model in backend/src/models/user_query.py to support selected text mode (depends on T017)
- [X] T030 [US2] Enhance retrieval service in backend/src/services/retrieval_service.py to support selected text mode (depends on T020)
- [X] T031 [US2] Update RAG service in backend/src/services/rag_service.py to handle selected text context (depends on T022)
- [X] T032 [US2] Implement text selection endpoint in backend/src/api/query_routes.py
- [X] T033 [US2] Implement session update endpoint to switch to selected text mode in backend/src/api/chat_routes.py
- [X] T034 [US2] Add validation and error handling for selected text queries
- [X] T035 [US2] Add logging for user story 2 operations

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Chat History and Session Management (Priority: P3)

**Goal**: Maintain conversation history with the chatbot to enable coherent, contextual discussions across multiple queries

**Independent Test**: The system can maintain and reference conversation history during a user session, allowing for follow-up questions that reference previous exchanges.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T036 [P] [US3] Contract test for session management endpoints in backend/tests/contract/test_session_api.py
- [X] T037 [P] [US3] Integration test for chat history flow in backend/tests/integration/test_chat_history.py

### Implementation for User Story 3

- [X] T038 [P] [US3] Create ChatSession model in backend/src/models/chat_session.py (depends on T007)
- [X] T039 [US3] Implement session service in backend/src/services/session_service.py
- [X] T040 [US3] Implement session creation endpoint in backend/src/api/chat_routes.py
- [X] T041 [US3] Implement chat history retrieval endpoint in backend/src/api/chat_routes.py
- [X] T042 [US3] Update UserQuery model to link with ChatSession (depends on T017, T038)
- [X] T043 [US3] Update RAG service to maintain session context (depends on T022)
- [X] T044 [US3] Add session validation and cleanup functionality
- [X] T045 [US3] Add logging for user story 3 operations

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T046 [P] Documentation updates in README.md
- [X] T047 [P] Create Dockerfile for deployment-ready configuration
- [X] T048 [P] Create .env.example file with all required environment variables
- [X] T049 Code cleanup and refactoring
- [X] T050 Performance optimization across all stories
- [X] T051 [P] Additional unit tests (if requested) in backend/tests/unit/
- [X] T052 Security hardening
- [X] T053 Run quickstart.md validation
- [X] T054 Implement ingestion endpoint for books in backend/src/api/book_routes.py
- [X] T055 Add proper citation functionality to ensure responses include source locations
- [X] T056 Implement zero hallucination checks to ensure responses only contain book content
- [X] T057 Add error handling for external service failures (Cohere, Qdrant)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May build on US1 components but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /query endpoint in backend/tests/contract/test_query_api.py"
Task: "Integration test for full book query flow in backend/tests/integration/test_full_book_query.py"

# Launch all models for User Story 1 together:
Task: "Create BookContent model in backend/src/models/book_content.py"
Task: "Create UserQuery model in backend/src/models/user_query.py"
Task: "Create RetrievedContext model in backend/src/models/retrieved_context.py"
Task: "Create GeneratedResponse model in backend/src/models/generated_response.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence