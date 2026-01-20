# 🚀 Portfolio API & Interactive Dashboard

A full-stack personal portfolio application built with **FastAPI**, **PostgreSQL**, and a responsive **HTML/JS Frontend**.
This project serves as a dynamic "Me API" that showcases education, projects, DSA problem stats, and certificates, wrapped in a beautiful dark-mode implementation.

> **[📄 View My Resume](https://drive.google.com/file/d/1z3qCo6t5DzglfBpeU3oUccKFGFu3wFbY/view?usp=sharing)**

---

## 🏗️ Architecture

The application is deployed as a consolidated web service on **Render**, connected to a cloud **Neon (PostgreSQL)** database.

```mermaid
graph TD
    Client[Browser / Mobile] -->|HTTPS| LoadBalancer[Render Load Balancer]
    LoadBalancer -->|API Requests| FastAPI[FastAPI Backend]
    LoadBalancer -->|Static Files| FastAPI
    
    FastAPI -->|Queries| NeonDB[(Neon PostgreSQL DB)]
    
    subgraph "Application Container"
        FastAPI
        Auth[Auth Middleware]
        Static[Static File Server]
    end
    
    Auth -.->|Validates| JWT[JWT Tokens]
```

---

## ✨ Features

### 👤 Multi-User & Admin System
*   **Secure Authentication**: Admin dashboard protected by JWT-based login (Bcrypt hashing).
*   **Multi-User Support**: Multiple users can create their own isolated portfolios (data privacy enforced by `user_id`).
*   **Data Isolation**: API automatically filters data based on the logged-in user or the requested profile ID.

### 🎨 Frontend & UX
*   **Dynamic Loading**: Single Page Application (SPA) feel using Vanilla JS.
*   **Responsive Design**: Mobile-friendly "Glassmorphism" UI with CSS variables/Tokens.
*   **Live Editing**: Admin dashboard allows creating, editing, and deleting records in real-time.
*   **Public/Private View**: Automatically switches between "Public Portfolio" view and "Admin Dashboard" view.

### 🔌 Backend API
*   **RESTful Design**: Properly structured endpoints for all resources.
*   **Search**: Global search functionality across projects and experiences.
*   **Documentation**: Auto-generated Swagger UI (`/docs`).

---

## 🛠️ Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| **Backend** | Python, FastAPI | High-performance async API framework. |
| **Database** | PostgreSQL, SQLAlchemy | Robust relational database with ORM. |
| **Auth** | OAuth2, JWT, Passlib | Secure token-based authentication. |
| **Frontend** | HTML5, CSS3, JavaScript | Lightweight, zero-dependency frontend. |
| **Deployment**| Docker, Render | Containerized deployment. |
| **Platform** | Neon (Serverless Postgres) | Cloud database provider. |

---

## 🗄️ Database Schema

The database consists of 5 main tables linked by Foreign Keys.

### 1. `BasicInfo` (User Profile)
The core profile table.
- `id` (PK), `full_name`, `email` (Unique), `bio`
- `phone`, `location`, `linkedin`, `github`, `leetcode`

### 2. `AdminUser` (Auth)
Stores login credentials.
- `id`, `username` (Unique), `hashed_password`
- `profile_id` (FK -> BasicInfo)

### 3. `Education`
- `institution`, `degree`, `field_of_study`
- `start_year`, `end_year`, `grade`, `description`
- `user_id` (FK)

### 4. `Project`
- `project_name`, `techstack` (Comma separated string)
- `description`, `project_url`
- `user_id` (FK)

### 5. `DSATopic`
Tracks DSA progress.
- `topic_name`, `category` ("Data Structure" / "Algorithm")
- `problems_solved` (List of stats), `resources`
- `user_id` (FK)

### 6. `Certificate`
- `title`, `issuer`, `issue_date`
- `credential_url`, `description`
- `user_id` (FK)

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- PostgreSQL (Local or Cloud)
- Docker (Optional)

### 1. Clone the Repository
```bash
git clone https://github.com/vidhishah2209/profile.git
cd profile
```

### 2. Environment Variables
Create a `.env` file in the root directory:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/profile_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Local Development (No Docker)
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run Database Migrations (if needed)
# alembic upgrade head

# Start Server
python -m uvicorn backend.main:app --reload
```
Visit `http://localhost:8000` to see the app.

### 4. Docker Build
```bash
# Build using the root context (Required for frontend copy)
docker build -f backend/Dockerfile -t my-portfolio .

# Run
docker run -p 8000:8000 -e DATABASE_URL=... my-portfolio
```

---

## 🌐 Deployment (Render)

This project is configured for seamless deployment on **Render**.

1.  **Create Web Service**: Connect your GitHub repo.
2.  **Settings**:
    *   **Runtime**: Docker
    *   **Root Directory**: `.` (Keep empty / Root)
    *   **Dockerfile Path**: `backend/Dockerfile`
3.  **Environment Variables**:
    *   Add `DATABASE_URL` (from your Neon/Postgres provider).
    *   Add `SECRET_KEY`.

---

## 📡 API Reference

Once running, full documentation is available at `/docs`.

### Key Endpoints
*   **Auth**: `POST /auth/login`, `POST /auth/register`
*   **Profile**: `GET /users/{id}`, `PUT /users/{id}`
*   **Education**: `GET /education?user_id=1`, `POST /education`
*   **Projects**: `GET /projects`, `POST /projects`
*   **DSA**: `GET /dsa`, `POST /dsa`

---

## ⚠️ Known Limitations
*   **Render Free Tier**: The server may spin down after 15 minutes of inactivity. The first request may take 30-50 seconds to load ("Cold Start").
*   **Media**: Does not strictly handle image uploads (uses URLs only).

---

## 📄 License
MIT License.
