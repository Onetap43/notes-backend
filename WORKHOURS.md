# WORKHOURS

> 
**Student:** Pranjal Singh  
**Project:** Full-Stack Notes Application (FastAPI + React)  
**Repository:** [Onetap43/notes-backend](https://github.com/Onetap43/notes-backend)

This retrospective log is based on my development history, deployment work, production testing, documentation work, and recollection of the time spent. No time spent reviewing Full Stack Open course material or passively following tutorials is included.

Git commits are used as development checkpoints, not as timers. The hours linked to development dates include the implementation, debugging, local testing, integration, and verification completed around those commits. Deployment, production verification, documentation review, and repository review may not always create a separate source-code commit and are therefore listed separately.

## Counted Development Work

| Date | Hours | Work done |
|---|---:|---|
| 12 May 2026 | 7.0 h | Set up the FastAPI project, cleaned the repository, created the User and Note database models, and added the first Pydantic schemas. |
| 13 May 2026 | 4.0 h | Integrated models and schemas with application startup, fixed initialization and import issues, and verified the basic backend flow. |
| 14 May 2026 | 3.5 h | Added authentication-related models and schemas and tested validation for signup and login data. |
| 15 May 2026 | 4.0 h | Developed the initial signup flow, adjusted authentication logic, and tested registration behavior. |
| 16 May 2026 | 8.0 h | Implemented signup, login, password hashing, JWT creation and validation, protected-route dependencies, and fixed related model and schema issues. |
| 17 May 2026 | 4.5 h | Implemented authenticated note creation with ownership validation, database persistence, error handling, and endpoint testing. |
| 18 May 2026 | 4.0 h | Implemented retrieval of all notes and a single note for the authenticated user, including ownership checks and not-found handling. |
| 19 May 2026 | 5.5 h | Implemented update and delete note endpoints with authorization checks, request validation, debugging, and testing. |
| 21 May 2026 | 5.0 h | Designed and implemented server-side pagination for notes and tested page, limit, and result behavior. |
| 22 May 2026 | 6.0 h | Implemented title and content search together with pin and unpin functionality, including the required database changes and testing. |
| 24 May 2026 | 5.0 h | Implemented archive and unarchive functionality, authorization checks, database state changes, and endpoint testing. |
| 25 May 2026 | 4.5 h | Added archived-notes retrieval and the recently updated notes feature, including ordering and timestamp verification. |
| 26 May 2026 | 7.5 h | Added database indexes, integrated login rate limiting, moved JWT settings to environment variables, updated dependencies, and tested the complete changes. |
| 01 Jun 2026 | 8.0 h | Implemented Docker support, created the container configuration, built images, and debugged container startup. |
| 02 Jun 2026 | 8.0 h | Migrated the application from SQLite to PostgreSQL using Docker Compose and resolved database connection and migration issues. |
| 04 Jun 2026 | 7.0 h | Refined PostgreSQL and Docker Compose integration, added logging support, implemented structured JSON logging, and tested the containerized application. |
| 05 Jun 2026 | 5.0 h | Created and debugged the GitHub Actions CI workflow and verified automated dependency and build checks. |
| 06 Jun 2026 | 1.5 h | Added and verified the API root and health response. |
| 07 Jun 2026 | 5.5 h | Fixed note-update datetime handling, corrected archived and recently updated routes, cleaned syntax, created the initial Postman collection, and tested backend endpoints. |
| 08 Jun 2026 | 6.5 h | Added SQLAlchemy connection pooling, finalized the Postman collection, and documented backend setup, API usage, Docker workflow, and project structure. |
| 16 Jun 2026 | 3.0 h | Diagnosed and fixed login rate-limiting behavior and verified correct HTTP 429 responses. |
| 12 Jul 2026 | 2.8 h | Initialized the React frontend with Vite, verified the environment, and removed the default starter content. |
| 13 Jul 2026 | 7.0 h | Created the frontend project structure, configured React Router, and integrated frontend login with FastAPI authentication and token storage. |
| 14 Jul 2026 | 8.0 h | Connected the dashboard to backend APIs and implemented the main notes dashboard, note creation, display, and management workflow. |
| 18 Jul 2026 | 6.5 h | Implemented frontend note update and delete functionality, forms, state updates, error handling, and related debugging. |
| 19 Jul 2026 | 6.0 h | Refactored the dashboard into reusable note components and verified application behavior after restructuring. |
| 22 Jul 2026 | 7.0 h | Refactored the notes dashboard, implemented the Archived Notes and Recently Updated pages, added restore interactions, and improved routing. |
| 23 Jul 2026 | 7.0 h | Integrated frontend search and pagination, improved dashboard UI and loading states, completed feature integration, configured the production API URL, and started deployment configuration. |
| 24 Jul 2026 | 5.0 h | Fixed the Archived page export, completed and debugged Vercel-to-Render CORS configuration, and adjusted production rate limiting. |
| 25 Jul 2026 | 3.5 h | Updated the final full-stack README with deployment links, application workflow, project structure, API documentation, and AI-use disclosure. |

**Counted development-work subtotal: 165.8 hours**

## Counted Deployment, Documentation, and Production Verification

These project activities did not necessarily create a separate source-code commit, but directly involved deploying, configuring, debugging, documenting, reviewing, or testing the project and its running application.

| Date | Hours | Work done |
|---|---:|---|
| 09 Jun 2026 | 3.0 h | Set up the backend and PostgreSQL service on Render, configured production environment variables, and verified service connectivity. |
| 10 Jun 2026 | 3.0 h | Investigated Render build and startup logs, corrected production configuration issues, redeployed the backend, and verified the live API and Swagger documentation. |
| 26 Jul 2026 | 3.0 h | Completed the platform-side Vercel deployment, configured production environment variables, and connected the deployed frontend to the Render backend. |
| 27 Jul 2026 | 1.5 h | Performed end-to-end testing on the deployed application, including authentication, CRUD operations, search, pagination, pinning, archiving, and recently updated notes. |
| 31 Jul 2026 | 2.0 h | Reviewed the repository code and project structure, checked the README against the project-submission requirements, corrected the documented API routes using the deployed Swagger interface, and verified the deployment, work-hours, and AI-disclosure links and wording. |

**Counted deployment, documentation, and production-verification subtotal: 12.5 hours**

## Supplementary Planning Record — Not Included in the Claimed Total

The following project-planning time is recorded for transparency, but it is deliberately excluded from the claimed project-hour total below.

| Date | Hours | Work done |
|---|---:|---|
| 07 May 2026 | 2.0 h | Planned the backend architecture, database flow, authentication flow, and overall project structure. |
| 09 May 2026 | 1.5 h | Defined the responsibilities of routes, models, schemas, database configuration, and application startup files. |
| 09 Jul 2026 | 1.5 h | Planned the frontend pages, reusable components, and API service organization. |
| 10 Jul 2026 | 1.5 h | Planned routing, authentication-state handling, and the responsibilities of the frontend files. |
| 11 Jul 2026 | 2.5 h | Mapped frontend actions to FastAPI endpoints and designed JWT and Axios request handling for the integration. |

**Planning time recorded but not claimed: 9.0 hours**

## Claimed Total

- Counted development work: **165.8 hours**
- Counted deployment, documentation, and production verification: **12.5 hours**
- **Claimed project total: 178.3 hours**
- Planning recorded separately and excluded: **9.0 hours**

> The claimed total excludes the supplementary planning entries and includes only the work listed in the two counted sections above. The 31 July entry reflects work actually completed on that date and is recorded separately from code-implementation commits.