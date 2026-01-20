# Me API Playground

A personal API playground to showcase your profile, experience, and projects with a beautiful interactive frontend.

## 🚀 Features

- **Profile Management** - Create and manage your personal profile
- **Experience Tracking** - Document your work history
- **Project Showcase** - Display your projects with tech stacks
- **Search** - Full-text search across all entities
- **Interactive Playground** - Test API endpoints in the browser

## 📁 Project Structure

```
me-api-playground/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── database.py      # Database configuration
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── crud.py          # CRUD operations
│   │   └── routes/          # API routes
│   ├── alembic/             # Database migrations
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   └── script.js
├── docker-compose.yml
├── seed.py
└── README.md
```

## 🛠️ Quick Start

### Using Docker

```bash
docker-compose up --build
```

- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

### Local Development

1. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

2. **Seed Database**
```bash
python seed.py
```

3. **Frontend**
Open `frontend/index.html` in your browser or serve with:
```bash
cd frontend
python -m http.server 3000
```

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/profile/ | List all profiles |
| GET | /api/profile/{id} | Get profile with details |
| POST | /api/profile/ | Create profile |
| PUT | /api/profile/{id} | Update profile |
| DELETE | /api/profile/{id} | Delete profile |
| GET | /api/experience/profile/{id} | List experiences |
| POST | /api/experience/ | Create experience |
| GET | /api/projects/profile/{id} | List projects |
| POST | /api/projects/ | Create project |
| GET | /api/search/?q={query} | Search all |

## 📝 License

MIT
