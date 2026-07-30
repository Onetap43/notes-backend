# WORKHOURS

**Student:** Pranjal Singh  
**Project:** Full-Stack Notes Application (FastAPI + React)  
**Repository:** [Onetap43/notes-backend](https://github.com/Onetap43/notes-backend)  
**Project period covered:** 7 May–25 July 2026

## Estimation Method

This is a retrospective work-hours estimate reconstructed from the exact Git commit history, project milestones, deployment work, and my recollection of the time spent.

A commit timestamp shows when completed work was saved to Git; it does not show when the work session began. A commit may therefore represent research, learning, implementation, debugging, and testing completed over one or more sessions before the commit. Small commits made close together are treated as parts of the same development session, which is shown by the daily subtotals below.

The commit-associated work totals **176 hours 30 minutes**. Planning, deployment setup, and final verification that did not produce a separate commit are recorded independently and total **20 hours**.

## Work Not Represented by a Separate Commit

| Period | Activity | Work Performed | Estimated Time |
|---|---|---|---:|
| 7–11 May 2026 | Backend architecture planning | Reviewed FastAPI project organization, responsibilities of the backend modules, database and authentication flow, and planned the initial backend structure. | 4 h |
| 9–12 July 2026 | Frontend architecture planning | Planned frontend pages, reusable components, routing, API service structure, authentication state, and the responsibility of each frontend file. | 3 h |
| 13–14 July 2026 | Backend–frontend integration planning | Mapped frontend actions to FastAPI endpoints, planned JWT and Axios handling, and designed the authenticated data flow. | 4 h |
| 8–16 June 2026 | Backend deployment and production setup | Deployed the backend and PostgreSQL database to Render, configured production variables, investigated build/startup issues, and verified the API and Swagger documentation. | 4 h |
| 23–25 July 2026 | Frontend deployment and production setup | Deployed the React frontend to Vercel, configured production variables, connected it to the deployed backend, and checked production behavior. | 3 h |
| 14–25 July 2026 | End-to-end verification not tied to one commit | Performed final manual testing of authentication, CRUD, pinning, archiving, recently updated notes, search, pagination, rate limiting, and production behavior. | 2 h |

**Non-commit work subtotal: 20 h**

## Commit-Associated Work Log

### 12 May 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `bcad5c9` | Initial clean project setup | Created the initial FastAPI repository structure, base files, database setup, and route placeholders. | 1 h |
| `c5ee838` | Update gitignore | Corrected `.gitignore` and removed generated environment/cache files committed accidentally. | 30 min |
| `a998a18` | Add user and note models | Designed and implemented the initial SQLAlchemy User and Note models and their relationship. | 4 h |
| `f852dc1` | Add Pydantic schemas | Created request and response schemas for validation and API serialization. | 3 h |
|  |  | **Daily subtotal** | **8 h 30 min** |

### 13 May 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `b47ecb3` | Add models schemas and app startup | Integrated the models and schemas with application startup and verified the initial backend flow. | 5 h |
|  |  | **Daily subtotal** | **5 h** |

### 14 May 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `6429030` | Add auth schemas and models | Added authentication-related schemas and model changes required for registration and login. | 2 h 30 min |
|  |  | **Daily subtotal** | **2 h 30 min** |

### 15 May 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `70c5979` | Updated auth and added partialsignup route | Developed the initial signup flow, adjusted authentication code, and tested registration behavior. | 2 h |
|  |  | **Daily subtotal** | **2 h** |

### 16 May 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `b7c748e` | Add signup login and JWT auth | Implemented signup, login, password hashing, JWT creation, authentication dependencies, and protected-route behavior. | 6 h |
| `8159e45` | Updated auth and models and schemas | Debugged and aligned authentication logic with the database models and Pydantic schemas. | 2 h |
|  |  | **Daily subtotal** | **8 h** |

### 17 May 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `feedbe8` | Added create note endpoint | Implemented authenticated note creation with ownership validation, persistence, and route testing. | 5 h |
|  |  | **Daily subtotal** | **5 h** |

### 18 May 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `e49404d` | Added get all notes route | Implemented retrieval of the authenticated user's notes and verified user-specific filtering. | 2 h 30 min |
| `87aef29` | Added Get specific note route | Implemented retrieval of an individual note with ownership and not-found handling. | 2 h |
|  |  | **Daily subtotal** | **4 h 30 min** |

### 19 May 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `8858012` | Added update and delete note endpoints | Implemented note update and deletion, including authorization checks, validation, debugging, and testing. | 5 h 30 min |
|  |  | **Daily subtotal** | **5 h 30 min** |

### 21 May 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `a76bc93` | Added pagination in get all notes route | Designed and implemented server-side pagination and verified page and limit behavior. | 4 h |
|  |  | **Daily subtotal** | **4 h** |

### 22 May 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `f713926` | Added search in get all notes route updated again | Implemented title/content search, refined the query behavior, and tested search with pagination. | 2 h 30 min |
| `c935f7b` | added pin route in notes and added boolean column in notes class in models.py | Added the pinned-state database field and implemented and tested pin/unpin behavior. | 2 h 30 min |
|  |  | **Daily subtotal** | **5 h** |

### 24 May 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `cac2596` | Add archive note feature | Added archive state to notes and implemented archive/unarchive behavior with testing. | 4 h |
|  |  | **Daily subtotal** | **4 h** |

### 25 May 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `2a75b2d` | Added Get Archived Notes | Implemented the archived-notes retrieval endpoint and user-specific filtering. | 1 h 30 min |
| `8a21674` | Added recently updated notes feature | Implemented recently updated note ordering/filtering and verified update timestamps. | 2 h 30 min |
|  |  | **Daily subtotal** | **4 h** |

### 26 May 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `6147866` | Added Indexes for note queries (Database Indexing) | Reviewed common query patterns, added indexes, and verified the database/model changes. | 2 h |
| `a5194c9` | Add login rate limiting | Integrated SlowAPI login rate limiting, configured middleware and handlers, and tested repeated requests. | 4 h |
| `f9912e5` | Load JWT settings from environment | Moved JWT configuration to environment variables and verified secure configuration loading. | 1 h 30 min |
| `51efaad` | Update project dependencies | Updated and checked backend dependencies after authentication and rate-limiting changes. | 30 min |
|  |  | **Daily subtotal** | **8 h** |

### 01 Jun 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `d5932d9` | Add Docker support | Learned and implemented Docker support, created the Docker configuration, built images, and debugged container startup across multiple sessions before the commit. | 8 h |
|  |  | **Daily subtotal** | **8 h** |

### 02 Jun 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `4fc4026` | Migrate from SQLite to PostgreSQL with Docker Compose | Migrated persistence from SQLite to PostgreSQL, configured Docker Compose, and resolved database connectivity and migration issues across multiple sessions. | 8 h 30 min |
|  |  | **Daily subtotal** | **8 h 30 min** |

### 04 Jun 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `2cd9fce` | Add PostgreSQL, Docker Compose and logging | Refined PostgreSQL and Compose integration, added logging support, and tested the containerized stack. | 4 h 30 min |
| `d0a4514` | Add structured JSON logging | Implemented structured JSON logs and verified request and application logging output. | 3 h 30 min |
|  |  | **Daily subtotal** | **8 h** |

### 05 Jun 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `ddd4af6` | Add GitHub Actions CI | Created and debugged the GitHub Actions workflow and verified automated build and dependency checks. | 5 h 30 min |
|  |  | **Daily subtotal** | **5 h 30 min** |

### 06 Jun 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `8655a51` | Add API root route | Added and verified the API root and health/information response. | 1 h 30 min |
|  |  | **Daily subtotal** | **1 h 30 min** |

### 07 Jun 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `f54767b` | fix update note datetime import | Investigated and fixed the datetime issue affecting note updates. | 1 h |
| `da53078` | Change archived notes route | Corrected archived-note route behavior and retested returned results. | 1 h |
| `f277285` | updated recently_updated route | Corrected and retested the recently-updated route. | 1 h |
| `1cbbe4d` | updated syntax | Performed small syntax corrections and cleanup found during testing. | 30 min |
| `e13ce2d` | Add Postman collection | Created the initial Postman collection, configured authenticated requests, and tested backend routes. | 3 h |
|  |  | **Daily subtotal** | **6 h 30 min** |

### 08 Jun 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `b5524e5` | Added connection pooling | Studied and configured SQLAlchemy connection pooling and tested database connection behavior. | 3 h 30 min |
| `2ac0bf2` | Add Postman collection | Expanded and finalized the Postman collection with endpoint coverage and request data. | 1 h 30 min |
| `743855d` | Add final README | Documented backend features, setup, API usage, Docker workflow, and project structure. | 2 h |
|  |  | **Daily subtotal** | **7 h** |

### 16 Jun 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `a87986d` | Fix login rate limiting | Diagnosed rate-limit behavior, corrected the implementation, and verified HTTP 429 responses. | 4 h |
|  |  | **Daily subtotal** | **4 h** |

### 12 Jul 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `0179914` | Initialize React frontend with Vite | Initialized the React/Vite application and verified the frontend development environment. | 1 h 30 min |
| `de32dd7` | Clean Vite starter template | Removed starter content and prepared a clean base for application development. | 1 h 30 min |
|  |  | **Daily subtotal** | **3 h** |

### 13 Jul 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `1290a39` | Create frontend project structure | Created the frontend page, component, service, and supporting file structure based on the prior plan. | 3 h |
| `26747e7` | Configure React Router and application routing | Configured routes and navigation for authentication, dashboard, archived, and recently updated pages. | 2 h 30 min |
| `eca18fd` | Integrate frontend login with FastAPI authentication | Integrated login requests, token storage, Axios authentication behavior, and error handling. | 2 h 30 min |
|  |  | **Daily subtotal** | **8 h** |

### 14 Jul 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `57677c7` | Connect dashboard with backend APIs | Connected dashboard requests to backend endpoints, handled authenticated fetching, and debugged responses. | 3 h 30 min |
| `a227ff1` | Implement dashboard and notes management | Built the main dashboard and note creation/display/management workflow and tested the core interactions. | 5 h |
|  |  | **Daily subtotal** | **8 h 30 min** |

### 18 Jul 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `fa3e980` | Add update and delete functionality to notes dashboard | Implemented frontend edit/delete interactions, forms, state updates, and related debugging over several work sessions. | 7 h |
|  |  | **Daily subtotal** | **7 h** |

### 19 Jul 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `0b816e9` | Refactor dashboard and add reusable note components | Refactored dashboard logic into reusable components and verified behavior after restructuring. | 7 h |
|  |  | **Daily subtotal** | **7 h** |

### 22 Jul 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `aaec0b5` | Refactor notes dashboard and add archived notes page done | Refactored dashboard code and implemented the Archived Notes page and restore interactions. | 4 h 30 min |
| `2b142d7` | Add recently updated notes page and improve app routing | Implemented the Recently Updated page and improved routing and navigation between views. | 3 h |
|  |  | **Daily subtotal** | **7 h 30 min** |

### 23 Jul 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `6321d44` | Add search pagination and improve dashboard UI | Integrated frontend search and pagination and improved dashboard presentation and loading states. | 3 h |
| `baf9051` | Complete notes app with search pagination and UI polish | Completed feature integration, fixed UI issues, and performed application-wide polish and regression checks. | 2 h 30 min |
| `3d585af` | Use environment variables for frontend API URL | Configured environment-based API URLs for local and deployed environments. | 1 h |
| `56e2527` | Configure CORS for frontend deployment | Configured backend CORS for production and investigated browser-origin failures. | 2 h |
|  |  | **Daily subtotal** | **8 h 30 min** |

### 24 Jul 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `a7a0d42` | Fix Archived page export | Diagnosed and corrected the Archived page export/import issue. | 1 h |
| `102bf97` | Allow deployed frontend in CORS | Updated the allowed production origin and verified the deployed request path. | 30 min |
| `655bbae` | Fix CORS for Vercel frontend | Debugged remaining Vercel-to-Render CORS issues and validated production requests. | 3 h 30 min |
| `d3ac993` | updated api rate limiting | Adjusted the production rate-limit configuration and retested login behavior. | 2 h |
|  |  | **Daily subtotal** | **7 h** |

### 25 Jul 2026

| Commit | Commit Message | Work Represented | Estimated Time |
|---|---|---|---:|
| `c74b736` | Readme updated | Updated final full-stack documentation, deployment links, workflow, AI-assistance disclosure, and project details. | 5 h |
|  |  | **Daily subtotal** | **5 h** |

**Commit-associated work subtotal (58 commits): 176 h 30 min**

## Final Summary

| Category | Time |
|---|---:|
| Commit-associated work | **176 h 30 min** |
| Work not represented by a separate commit | **20 h** |
| **Overall project work** | **196 h 30 min** |

## Total Working Hours

**Commit-associated work: 176 h 30 min (176.5 hours)**  
**Non-commit work: 20 h (20 hours)**  
**Overall total: 196 h 30 min (196.5 hours)**

