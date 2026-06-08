Notes Backend API

A production-style backend API built using FastAPI, PostgreSQL, Docker, JWT Authentication, SQLAlchemy, GitHub Actions, and Render Deployment.

The application allows users to securely create, update, delete, pin, archive, and manage personal notes through authenticated REST APIs.

Project Overview

This project was built to learn and apply industry-level backend development practices.

The backend includes authentication, database design, Docker containerization, cloud deployment, structured logging, database optimization, API security, and CI workflows.

Users can manage personal notes while ensuring data isolation through user-specific authentication.



Highlights

- JWT Authentication
- PostgreSQL Database
- Dockerized Application
- GitHub Actions CI
- Cloud Deployment on Render
- API Rate Limiting
- Database Indexing
- Connection Pooling
- Structured JSON Logging
- Swagger Documentation
- Postman Collection



Features

Authentication & Security

- User Signup
- User Login
- JWT Authentication
- Password Hashing using bcrypt
- Protected Routes
- Environment Variables
- API Rate Limiting

Notes Management

- Create Note
- Get All Notes
- Get Specific Note
- Update Note
- Delete Note

Advanced Features

- Pin / Unpin Notes
- Archive / Unarchive Notes
- Recently Updated Notes
- User Profile Endpoint

Performance & Scalability

- PostgreSQL Database
- SQLAlchemy ORM
- Database Connection Pooling
- Database Indexing
- Structured JSON Logging

DevOps & Deployment

- Dockerized Application
- Docker Compose Support
- GitHub Actions CI
- Cloud Deployment on Render
- Interactive Swagger Documentation
- Postman Collection



Tech Stack

Backend

- Python
- FastAPI

Database

- PostgreSQL
- SQLAlchemy

Authentication

- JWT
- Passlib (bcrypt)

DevOps

- Docker
- Docker Compose
- GitHub Actions
- Render

API Testing

- Swagger UI
- Postman



Repository

https://github.com/Onetap43/notes-backend



API Endpoints

Authentication

Method| Endpoint| Description
POST| /signup| Create account
POST| /login| User login

Notes

Method| Endpoint| Description
POST| /notes| Create note
GET| /notes| Get all notes
GET| /notes/{note_id}| Get specific note
PUT| /update_notes/{note_id}| Update note
DELETE| /notes/{note_id}| Delete note

Additional Features

Method| Endpoint| Description

PATCH| /notes/{note_id}/pin| Toggle pin
PATCH| /notes/{note_id}/archive| Archive note
GET| /archived_notes| Get archived notes
GET| /recently_updated| Recently updated notes
GET| /me| Current user profile



Project Structure

notes-backend/
│
├── .github/
│   └── workflows/
│
├── app/
│   ├── routes/
│   ├── auth.py
│   ├── database.py
│   ├── logger.py
│   ├── limiter.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
│
├── postman/
│   └── notes_backend_postman_collection.json
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .env



Local Setup

Clone the repository:

git clone https://github.com/Onetap43/notes-backend.git

Move into project folder:

cd notes-backend

Install dependencies:

pip install -r requirements.txt

Run the server:

uvicorn app.main:app --reload



Docker Setup

Build and run containers:

docker compose up --build

Run existing containers:

docker compose up

---

Live Deployment

Live API

https://notes-backend-fhvg.onrender.com

Swagger Documentation

https://notes-backend-fhvg.onrender.com/docs



Postman Collection

The complete Postman collection is available in:

postman/notes_backend_postman_collection.json

Import the collection directly into Postman to test all API endpoints.



CI/CD

This project uses GitHub Actions for Continuous Integration.

On every push to the main branch, the GitHub Actions workflow runs automated checks to verify that dependencies install correctly and important project imports work.

The project is deployed on Render, and Render is connected to the GitHub repository for cloud deployment.



Logging

Structured JSON logging has been implemented for:

- Authentication events
- Login attempts
- Note creation
- Note updates
- Note deletion
- API requests



Database

PostgreSQL is used as the primary database.

Implemented database features:

- SQLAlchemy ORM
- Connection Pooling
- Database Indexing
- Session Management



What I Learned

Through this project I gained practical experience with:

- FastAPI Backend Development
- REST API Design
- JWT Authentication
- Password Security using bcrypt
- PostgreSQL Database Design
- SQLAlchemy ORM
- Docker Containerization
- GitHub Actions CI
- Cloud Deployment
- Structured Logging
- Connection Pooling
- Database Indexing
- Rate Limiting
- Git and GitHub Workflows
- API Testing using Postman



Future Improvements

- Full Text Search
- Note Categories
- Refresh Token Authentication
- Email Verification
- Password Reset Functionality
- Automated Testing
- Monitoring and Metrics Dashboard


Author:

Pranjal Singh

Computer Science and Engineering

University of Oulu

Backend project built to practice industry-level backend engineering concepts.