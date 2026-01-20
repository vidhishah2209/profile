from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
import os
import models
import schemas
import crud
from database import engine, SessionLocal
from auth import get_password_hash, verify_password, create_access_token, get_current_user

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Personal Portfolio API",
    description="API for managing personal portfolio with education, projects, DSA topics, and certificates",
    version="2.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get frontend directory path
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")


# Root route to serve frontend
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# Serve static files (script.js, etc.)
@app.get("/script.js")
def serve_script():
    return FileResponse(os.path.join(FRONTEND_DIR, "script.js"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------- HEALTH CHECK --------
@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "ok", "database": "disconnected", "error": str(e)}


# -------- AUTHENTICATION --------
@app.post("/auth/register", response_model=schemas.Token)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new admin user with their own empty portfolio"""
    # Check if user already exists
    existing = db.query(models.AdminUser).filter(models.AdminUser.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create a new empty profile (BasicInfo) for this user
    new_profile = models.BasicInfo(
        full_name=user.username,  # Default name is username
        email=f"{user.username}@example.com"  # Placeholder email
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    
    # Create new admin user linked to the profile
    hashed_password = get_password_hash(user.password)
    db_user = models.AdminUser(
        username=user.username, 
        hashed_password=hashed_password,
        profile_id=new_profile.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate token with profile_id
    access_token = create_access_token(data={"sub": user.username, "user_id": db_user.id, "profile_id": new_profile.id})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/auth/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """Login and get access token"""
    db_user = db.query(models.AdminUser).filter(models.AdminUser.username == user.username).first()
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Include profile_id in token for data isolation
    profile_id = db_user.profile_id if db_user.profile_id else 1  # Default to 1 for legacy users
    access_token = create_access_token(data={"sub": user.username, "user_id": db_user.id, "profile_id": profile_id})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/auth/me", response_model=schemas.UserOut)
def get_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current authenticated user"""
    db_user = db.query(models.AdminUser).filter(models.AdminUser.username == current_user["sub"]).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# -------- BASIC INFO --------
@app.post("/users", response_model=schemas.BasicInfoOut)
def create_user(user: schemas.BasicInfoCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@app.get("/users/{user_id}", response_model=schemas.BasicInfoOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=schemas.BasicInfoOut)
def update_user(user_id: int, user_update: schemas.BasicInfoUpdate, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -------- EDUCATION --------
@app.post("/education", response_model=schemas.EducationOut)
def add_education(
    edu: schemas.EducationCreate, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Force user_id from token
    edu.user_id = current_user["profile_id"]
    return crud.create_education(db, edu)


@app.get("/education", response_model=List[schemas.EducationOut])
def list_education(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_education_list(db, user_id)


@app.get("/education/{edu_id}", response_model=schemas.EducationOut)
def get_education(edu_id: int, db: Session = Depends(get_db)):
    edu = crud.get_education(db, edu_id)
    if not edu:
        raise HTTPException(status_code=404, detail="Education not found")
    return edu


@app.put("/education/{edu_id}", response_model=schemas.EducationOut)
def update_education(
    edu_id: int, 
    edu_update: schemas.EducationUpdate, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify ownership
    existing_edu = crud.get_education(db, edu_id)
    if not existing_edu:
        raise HTTPException(status_code=404, detail="Education not found")
    if existing_edu.user_id != current_user["profile_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this item")
        
    return crud.update_education(db, edu_id, edu_update)


@app.delete("/education/{edu_id}")
def delete_education(
    edu_id: int, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify ownership
    existing_edu = crud.get_education(db, edu_id)
    if not existing_edu:
        raise HTTPException(status_code=404, detail="Education not found")
    if existing_edu.user_id != current_user["profile_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this item")
        
    crud.delete_education(db, edu_id)
    return {"status": "deleted"}


# -------- PROJECTS --------
@app.post("/projects", response_model=schemas.ProjectOut)
def add_project(
    project: schemas.ProjectCreate, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project.user_id = current_user["profile_id"]
    return crud.create_project(db, project)


@app.get("/projects", response_model=List[schemas.ProjectOut])
def list_projects(
    techstack: Optional[str] = Query(None, description="Filter by techstack"),
    sorted: bool = Query(False, description="Sort alphabetically"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db)
):
    if techstack:
        return crud.filter_projects_by_techstack(db, techstack)
    if sorted:
        return crud.get_projects_sorted(db, user_id)
    return crud.get_projects(db, user_id)


@app.get("/projects/{proj_id}", response_model=schemas.ProjectOut)
def get_project(proj_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, proj_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.put("/projects/{proj_id}", response_model=schemas.ProjectOut)
def update_project(
    proj_id: int, 
    proj_update: schemas.ProjectUpdate, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exists = crud.get_project(db, proj_id)
    if not exists:
        raise HTTPException(status_code=404, detail="Project not found")
    if exists.user_id != current_user["profile_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this item")
        
    return crud.update_project(db, proj_id, proj_update)


@app.delete("/projects/{proj_id}")
def delete_project(
    proj_id: int, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exists = crud.get_project(db, proj_id)
    if not exists:
        raise HTTPException(status_code=404, detail="Project not found")
    if exists.user_id != current_user["profile_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this item")

    crud.delete_project(db, proj_id)
    return {"message": "Project deleted successfully"}


# -------- DSA TOPICS --------
@app.post("/dsa", response_model=schemas.DSATopicOut)
def add_dsa_topic(
    topic: schemas.DSATopicCreate, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    topic.user_id = current_user["profile_id"]
    return crud.create_dsa_topic(db, topic)


@app.get("/dsa", response_model=List[schemas.DSATopicOut])
def list_dsa_topics(
    category: Optional[str] = Query(None, description="Filter by category"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db)
):
    return crud.get_dsa_topics(db, user_id=user_id, category=category)


@app.get("/dsa/{topic_id}", response_model=schemas.DSATopicOut)
def get_dsa_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = crud.get_dsa_topic(db, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="DSA topic not found")
    return topic


@app.put("/dsa/{topic_id}", response_model=schemas.DSATopicOut)
def update_dsa_topic(
    topic_id: int, 
    topic_update: schemas.DSATopicUpdate, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exists = crud.get_dsa_topic(db, topic_id)
    if not exists:
        raise HTTPException(status_code=404, detail="DSA topic not found")
    if exists.user_id != current_user["profile_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this item")
        
    return crud.update_dsa_topic(db, topic_id, topic_update)


@app.delete("/dsa/{topic_id}")
def delete_dsa_topic(
    topic_id: int, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exists = crud.get_dsa_topic(db, topic_id)
    if not exists:
        raise HTTPException(status_code=404, detail="DSA topic not found")
    if exists.user_id != current_user["profile_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this item")

    crud.delete_dsa_topic(db, topic_id)
    return {"message": "DSA topic deleted successfully"}


# -------- CERTIFICATES --------
@app.post("/certificates", response_model=schemas.CertificateOut)
def add_certificate(
    cert: schemas.CertificateCreate, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cert.user_id = current_user["profile_id"]
    return crud.create_certificate(db, cert)


@app.get("/certificates", response_model=List[schemas.CertificateOut])
def list_certificates(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_certificates(db, user_id)


@app.get("/certificates/{cert_id}", response_model=schemas.CertificateOut)
def get_certificate(cert_id: int, db: Session = Depends(get_db)):
    cert = crud.get_certificate(db, cert_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return cert


@app.put("/certificates/{cert_id}", response_model=schemas.CertificateOut)
def update_certificate(
    cert_id: int, 
    cert_update: schemas.CertificateUpdate, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exists = crud.get_certificate(db, cert_id)
    if not exists:
        raise HTTPException(status_code=404, detail="Certificate not found")
    if exists.user_id != current_user["profile_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this item")

    return crud.update_certificate(db, cert_id, cert_update)


@app.delete("/certificates/{cert_id}")
def delete_certificate(
    cert_id: int, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exists = crud.get_certificate(db, cert_id)
    if not exists:
        raise HTTPException(status_code=404, detail="Certificate not found")
    if exists.user_id != current_user["profile_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this item")

    crud.delete_certificate(db, cert_id)
    return {"message": "Certificate deleted successfully"}


# -------- SEARCH --------
@app.get("/search")
def search(q: str = Query(..., description="Search query"), db: Session = Depends(get_db)):
    if not q or len(q) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    results = crud.search_all(db, q)
    return {
        "query": q,
        "projects": [schemas.ProjectOut.model_validate(p) for p in results["projects"]],
        "dsa_topics": [schemas.DSATopicOut.model_validate(t) for t in results["dsa_topics"]]
    }
