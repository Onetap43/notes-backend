> **AI disclosure:** OpenAI ChatGPT assisted with code generation, implementation, debugging, automated tests, and documentation. See [AI Assistance](#-ai-assistance) for details. The author ran automated and manual tests and is responsible for project verification and submission.

# 📝 Notes App

A full-stack **Notes Management Application** built using **FastAPI**, **React**, and **PostgreSQL**. The base application is deployed, while the tags, checklists, version history, and automated-test expansion is being prepared for production. The code includes JWT authentication, note management, search, pagination, pinning, archiving, tags, checklists, version history, API rate limiting, structured logging, Docker support, and cloud deployment.



# 🚀 A Live Demo

### Frontend (existing production deployment; expansion not yet verified live)

https://notes-backend-project.vercel.app

### Backend API (existing production deployment)

https://notes-backend-fhvg.onrender.com

### Swagger Documentation

https://notes-backend-fhvg.onrender.com/docs



# 📌 Project Overview

The Notes App allows users to securely create and manage their personal notes.

Each user has their own private notes protected using JWT Authentication. After logging in, users can create, update, delete, search, pin, archive, tag, and organize notes with checklists and version history. The backend is built using FastAPI with SQLAlchemy ORM, while the frontend is developed using React and Vite. The existing application is deployed on Render and Vercel. At the time of the expansion PR, the new features have been tested locally but are not yet verified in production.

# 📖 How to Use

1. Open the deployed frontend.
2. Create an account from the signup page.
3. Log in using your username and password.
4. Create, edit, delete, pin, or archive personal notes.
5. Use the search bar and pagination to find notes.
6. Create tags, assign tags to notes, and filter your dashboard by tag.
7. Open a note checklist to add, edit, complete, and remove tasks.
8. Edit a note and use Version History to inspect and restore an earlier title/content.
9. Open the Archived and Recently Updated pages from the navigation menu.



# ✨ Features

## 🔐 Authentication

- User Signup
- User Login
- JWT Authentication
- Password Hashing using bcrypt
- Protected API Routes
- Current User Profile



## 📝 Notes Management

- Create Notes
- View Notes
- Edit Notes
- Delete Notes
- Pin / Unpin Notes
- Archive / Unarchive Notes
- Recently Updated Notes



## 🏷️ Tags & Categories

- User-owned tags: create, view, and delete tags
- Assign multiple tags to a note, and remove assignments
- Filter dashboard notes using a tag
- Restrict tag and note access to the authenticated owner

## ✅ Note Checklists

- Add, edit, complete/uncomplete, and delete checklist items per note
- Track completion count and progress percentage
- Persist checklist items in the database

## 🕓 Note Version History

- Save the previous title and content when a note is changed
- List previous versions with timestamps
- Restore an earlier version while preserving the replaced current state
- Enforce ownership on version-history endpoints

## 🔍 Search & Pagination

- Search notes by title or content
- Server-side Pagination
- Faster data retrieval



## 🛡️ Security

- JWT Authentication
- Password Hashing using bcrypt
- Protected API Endpoints
- Login API Rate Limiting (SlowAPI)
- CORS Configuration

## 🗄️ Database

- PostgreSQL
- SQLAlchemy ORM
- SQLAlchemy Connection Pooling
- Pool health checks using `pool_pre_ping`
- Automatic table creation via SQLAlchemy `create_all()` on backend startup
- User-Note Relationship Management
- New tables: `tags`, `note_tags`, `checklist_items`, `note_versions`
- Existing `users` and `notes` table definitions remain unchanged by this expansion

**Deployment note:** `create_all()` creates missing tables but does not upgrade existing columns. Production verification and a database backup are required before accepting this release as fully deployed.



## ⚙️ Production Features

- Docker Support
- GitHub Actions CI Pipeline (backend `pytest`, Python checks, frontend lint/build)
- Structured Logging
- Environment Variables
- Cloud Deployment

# 🔄 Database Connection Pooling

The backend uses SQLAlchemy connection pooling to reuse existing database
connections instead of creating a new connection for every request.

The configured pool uses:

- `pool_size=5` for persistent database connections
- `max_overflow=10` for temporary additional connections during higher load
- `pool_pre_ping=True` to verify connections before reuse and replace stale connections

This improves database efficiency and helps maintain reliable connections in
the deployed PostgreSQL environment.

# 🛠 Tech Stack

| Layer | Technology |
|--------|------------|
| Frontend | React, Vite, React Router, Axios |
| Backend | FastAPI, SQLAlchemy |
| Database | PostgreSQL |
| Authentication | JWT, Passlib (bcrypt) |
| Rate Limiting | SlowAPI |
| DevOps | Docker, GitHub Actions |
| Deployment | Render, Vercel |
| Version Control | Git & GitHub |


# 📂 Project Structure

```text
notes-backend/
│
├── app/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── notes.py
│   │   ├── tags.py
│   │   ├── checklists.py
│   │   └── history.py
│   ├── database.py
│   ├── limiter.py
│   ├── logger.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
├── .github/
│   └── workflows/
│       └── ci.yml
├── postman/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── WORKHOURS.md
├── WORKHOURS_10ECTS.md
├── tests/
│   ├── conftest.py
│   ├── test_notes_api.py
│   ├── test_tags_api.py
│   ├── test_checklists_api.py
│   └── test_history_api.py
├── README.md
└── .gitignore
```

# ⚙️ Application Workflow

## 1. User Signup

- User enters a username and password.
- Password is hashed using bcrypt.
- User information is securely stored in PostgreSQL.



## 2. User Login

- Username and password are verified.
- FastAPI generates a JWT Access Token.
- Token is returned to the frontend.
- React stores the token in Local Storage.
- Login endpoint is protected using API Rate Limiting to reduce brute-force login attempts.



## 3. Authentication

Every protected API request automatically includes:

```http
Authorization: Bearer <JWT_TOKEN>
```

using an Axios Interceptor.

FastAPI verifies the JWT before allowing access to protected endpoints.



## 4. Notes Management

After successful authentication, users can:

- Create notes
- View notes
- Edit notes
- Delete notes
- Pin or Unpin notes
- Archive or Unarchive notes

Every note belongs only to the authenticated user.



## 5. Search

Users can search notes using keywords.

The backend filters matching notes and returns only relevant results.



## 6. Pagination

Notes are divided into pages on the backend to improve performance and reduce unnecessary data transfer.



## 7. Recently Updated

Recently modified notes are displayed separately, allowing users to quickly access their latest work.



# 🔐 Security Features

- JWT Authentication
- Password Hashing using bcrypt
- Protected API Endpoints
- Login API Rate Limiting (SlowAPI)
- CORS Protection
- Environment Variables

## CI/CD

The project uses GitHub Actions for backend validation, **18 automated API tests**, frontend ESLint, Vite production builds, and a Render deployment hook on push to `main`.

Run checks locally from the repository root:

```bash
python -m pytest tests -v
cd frontend
npm ci
npm run lint
npm run build
```

At the time of the expansion PR, **18/18 backend tests passed locally**, the frontend lint/build passed, and the new features were manually tested locally. Production deployment must be verified separately. Tests include authentication, note CRUD/ownership/pagination, tags, checklists, and history/restore.



# 📡 API Endpoints

## Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/signup` | Register a new user |
| POST | `/login` | Authenticate user and generate JWT |
| GET | `/me` | Get authenticated user profile |

## Notes

| Method | Endpoint | Description |
|---|---|---|
| POST | `/notes` | Create a note |
| GET | `/notes` | Retrieve the authenticated user's notes with search and pagination support |
| GET | `/notes/{note_id}` | Get a specific note |
| DELETE | `/notes/{note_id}` | Delete a note |
| PUT | `/update_notes/{note_id}` | Update a note |
| PATCH | `/notes/{note_id}/pin` | Pin or unpin a note |
| PATCH | `/notes/{note_id}/archive` | Archive or unarchive a note |
| GET | `/archived_notes` | Get archived notes |
| GET | `/recently_updated` | Get recently updated notes |

## Tags

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tags` | Create a tag |
| GET | `/tags` | List own tags |
| DELETE | `/tags/{tag_id}` | Delete a tag |
| PUT | `/notes/{note_id}/tags/{tag_id}` | Assign tag to a note |
| DELETE | `/notes/{note_id}/tags/{tag_id}` | Remove tag assignment |
| GET | `/notes/{note_id}/tags` | List note tags |
| GET | `/tags/{tag_id}/notes` | List notes with a tag |

## Checklists

| Method | Endpoint | Description |
|---|---|---|
| GET | `/notes/{note_id}/checklist` | List items and progress |
| POST | `/notes/{note_id}/checklist` | Add item |
| PATCH | `/notes/{note_id}/checklist/{item_id}` | Update item or completion |
| DELETE | `/notes/{note_id}/checklist/{item_id}` | Delete item |

## Version History

| Method | Endpoint | Description |
|---|---|---|
| GET | `/notes/{note_id}/history` | List previous versions |
| POST | `/notes/{note_id}/history/{version_id}/restore` | Restore previous version |

## General

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API home route |
| GET | `/health` | Health check |

## Work Hours

The detailed work-hours log is available directly in the repository:

[View the work-hours log](./WORKHOURS.md)

The original project work-hours file records **178.3 hours**. The separate [10 ECTS expansion log](./WORKHOURS_10ECTS.md) records **5.5 additional hours as of 21 October 2026**, for **183.8 total documented hours** at that point.

Supplementary planning time is documented separately in the original work-hours file and is not included in the claimed original total.

# ⚙️ Environment Variables

## Backend

```env
DATABASE_URL=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
```

## Frontend

```env
VITE_API_URL=
```

---

# 🐳 Docker

The backend supports Docker deployment.

```bash
docker-compose up --build
```

---

# ☁️ Deployment

### Backend

- Render

### Frontend

- Vercel

### Database

- PostgreSQL (Render)

---

# 📈 Future Improvements

- Password Reset
- Email Verification
- Rich Text Notes
- Note Sharing
- Dark Mode
- Refresh Tokens
- Redis Caching
- Additional frontend component tests
- Expanded integration and deployment tests
- User Profile Management

---

# 👨‍💻 Author

**Pranjal Singh**

Computer Science & Engineering Student

University of Oulu

GitHub: https://github.com/Onetap43

---

# 🤖 AI Assistance

OpenAI ChatGPT was used substantially as a development assistant. Assistance included explaining concepts, generating or revising code and tests, providing multi-file feature patches, debugging, CI configuration, API design, and documentation. The author applied the changes, ran automated and manual tests, verified behavior locally, and maintained the repository.

In particular, the following expansion areas were implemented with significant AI-assisted code generation and review:

- **Backend:** `app/models.py`, `app/main.py`, `app/routes/tags.py`, `app/routes/checklists.py`, `app/routes/history.py`, and changes to `app/routes/notes.py`
- **Frontend:** `frontend/src/components/TagsPanel.jsx`, `Checklist.jsx`, `VersionHistory.jsx`, `NoteCard.jsx`, and changes to `frontend/src/pages/Dashboard/Dashboard.jsx`
- **Tests:** `tests/conftest.py`, `tests/test_notes_api.py`, `tests/test_tags_api.py`, `tests/test_checklists_api.py`, and `tests/test_history_api.py`
- **DevOps/documentation:** `.github/workflows/ci.yml`, `README.md`, and troubleshooting guidance

The original application also received AI assistance for authentication, backend/frontend programming, deployment configuration, and debugging. The extent of assistance is disclosed here so that the reviewer can assess the work transparently.

---

# 📄 License

This project was developed for educational purposes and portfolio demonstration.
