> **AI disclosure:** This README was generated with the assistance of OpenAI ChatGPT. It was reviewed, corrected, and approved by the author.

# 📝 Notes App

A deployed full-stack **Notes Management Application** built using **FastAPI**, **React**, and **PostgreSQL**. The application provides secure JWT authentication, complete note management, search, pagination, pinning, archiving, API rate limiting, structured logging, Docker support, and cloud deployment.



# 🚀 A Live Demo

### Frontend

https://notes-backend-project.vercel.app

### Backend API

https://notes-backend-fhvg.onrender.com

### Swagger Documentation

https://notes-backend-fhvg.onrender.com/docs



# 📌 Project Overview

The Notes App allows users to securely create and manage their personal notes.

Each user has their own private notes protected using JWT Authentication. After logging in, users can create, update, delete, search, pin, and archive notes. The backend is built using FastAPI with SQLAlchemy ORM, while the frontend is developed using React and Vite. The complete application is deployed on Render and Vercel.

# 📖 How to Use

1. Open the deployed frontend.
2. Create an account from the signup page.
3. Log in using your username and password.
4. Create, edit, delete, pin, or archive personal notes.
5. Use the search bar and pagination to find notes.
6. Open the Archived and Recently Updated pages from the navigation menu.



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
- Automatic Table Creation
- User-Note Relationship Management



## ⚙️ Production Features

- Docker Support
- GitHub Actions CI Pipeline
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
│   │   └── notes.py
│   ├── database.py
│   ├── dependencies.py
│   ├── limiter.py
│   ├── logger.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
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

## General

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API home route |

## Work Hours

The detailed work-hours log is available directly in the repository:

[View the work-hours log](./WORKHOURS.md)

The claimed project total is **178.3 hours**.

Supplementary planning time is documented separately in the work-hours file but is not included in the claimed total.

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
- Tags & Categories
- Note Sharing
- Dark Mode
- Refresh Tokens
- Redis Caching
- Unit Testing
- Integration Testing
- User Profile Management

---

# 👨‍💻 Author

**Pranjal Singh**

Computer Science & Engineering Student

University of Oulu

GitHub: https://github.com/Onetap43

---

# 🤖 AI Assistance

OpenAI ChatGPT was used as a development assistant throughout this project.

AI assistance was used for:

- Explaining backend and frontend concepts
- Debugging errors and fixing issues
- Suggesting implementation approaches
- Improving code structure and readability
- Writing and improving project documentation
- Reviewing deployment configurations
- Providing development best practices

All AI-generated code and suggestions were reviewed, modified, tested, and integrated by the author before being committed and deployed.

---

# 📂 AI-Assisted Files

The following files received AI assistance during development:

## Backend

- app/main.py
- app/logger.py

## Frontend

- frontend/src/pages/Login.jsx
- frontend/src/pages/Signup.jsx
## DevOps & Documentation

- docker-compose.yml
- .github/workflows/ci.yml
- README.md


AI assistance included code suggestions, debugging support, documentation improvements, implementation guidance, and best practices. Final project architecture, integration, testing, deployment, verification, and maintenance were completed by the author.

---

# 📄 License

This project was developed for educational purposes and portfolio demonstration.
