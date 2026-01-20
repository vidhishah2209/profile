from sqlalchemy.orm import Session
from sqlalchemy import or_
import models
import schemas


# ---------- BASIC INFO ----------
def create_user(db: Session, user: schemas.BasicInfoCreate):
    db_user = models.BasicInfo(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.BasicInfo).filter(models.BasicInfo.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.BasicInfo).filter(models.BasicInfo.email == email).first()


def update_user(db: Session, user_id: int, user_update: schemas.BasicInfoUpdate):
    db_user = db.query(models.BasicInfo).filter(models.BasicInfo.id == user_id).first()
    if not db_user:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---------- EDUCATION ----------
def create_education(db: Session, edu: schemas.EducationCreate):
    db_edu = models.Education(**edu.model_dump())
    db.add(db_edu)
    db.commit()
    db.refresh(db_edu)
    return db_edu


def get_education_list(db: Session, user_id: int = None):
    query = db.query(models.Education)
    if user_id:
        query = query.filter(models.Education.user_id == user_id)
    return query.order_by(models.Education.end_year.desc()).all()


def get_education(db: Session, edu_id: int):
    return db.query(models.Education).filter(models.Education.id == edu_id).first()


def update_education(db: Session, edu_id: int, edu_update: schemas.EducationUpdate):
    db_edu = db.query(models.Education).filter(models.Education.id == edu_id).first()
    if not db_edu:
        return None
    update_data = edu_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_edu, key, value)
    db.commit()
    db.refresh(db_edu)
    return db_edu


def delete_education(db: Session, edu_id: int):
    db_edu = db.query(models.Education).filter(models.Education.id == edu_id).first()
    if not db_edu:
        return False
    db.delete(db_edu)
    db.commit()
    return True


# ---------- PROJECT ----------
def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(db: Session, user_id: int = None):
    query = db.query(models.Project)
    if user_id:
        query = query.filter(models.Project.user_id == user_id)
    return query.all()


def get_project(db: Session, proj_id: int):
    return db.query(models.Project).filter(models.Project.id == proj_id).first()


def update_project(db: Session, proj_id: int, proj_update: schemas.ProjectUpdate):
    db_project = db.query(models.Project).filter(models.Project.id == proj_id).first()
    if not db_project:
        return None
    update_data = proj_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, proj_id: int):
    db_project = db.query(models.Project).filter(models.Project.id == proj_id).first()
    if not db_project:
        return False
    db.delete(db_project)
    db.commit()
    return True


def filter_projects_by_techstack(db: Session, techstack: str):
    return db.query(models.Project).filter(
        models.Project.techstack.ilike(f"%{techstack}%")
    ).all()


def get_projects_sorted(db: Session, user_id: int = None):
    query = db.query(models.Project)
    if user_id:
        query = query.filter(models.Project.user_id == user_id)
    return query.order_by(models.Project.project_name.asc()).all()


# ---------- DSA TOPIC ----------
def create_dsa_topic(db: Session, topic: schemas.DSATopicCreate):
    db_topic = models.DSATopic(**topic.model_dump())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def get_dsa_topics(db: Session, user_id: int = None, category: str = None):
    query = db.query(models.DSATopic)
    if user_id:
        query = query.filter(models.DSATopic.user_id == user_id)
    if category:
        query = query.filter(models.DSATopic.category.ilike(f"%{category}%"))
    return query.order_by(models.DSATopic.category, models.DSATopic.topic_name).all()


def get_dsa_topic(db: Session, topic_id: int):
    return db.query(models.DSATopic).filter(models.DSATopic.id == topic_id).first()


def update_dsa_topic(db: Session, topic_id: int, topic_update: schemas.DSATopicUpdate):
    db_topic = db.query(models.DSATopic).filter(models.DSATopic.id == topic_id).first()
    if not db_topic:
        return None
    update_data = topic_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_topic, key, value)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def delete_dsa_topic(db: Session, topic_id: int):
    db_topic = db.query(models.DSATopic).filter(models.DSATopic.id == topic_id).first()
    if not db_topic:
        return False
    db.delete(db_topic)
    db.commit()
    return True


# ---------- CERTIFICATE ----------
def create_certificate(db: Session, cert: schemas.CertificateCreate):
    db_cert = models.Certificate(**cert.model_dump())
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert


def get_certificates(db: Session, user_id: int = None):
    query = db.query(models.Certificate)
    if user_id:
        query = query.filter(models.Certificate.user_id == user_id)
    return query.order_by(models.Certificate.issue_date.desc()).all()


def get_certificate(db: Session, cert_id: int):
    return db.query(models.Certificate).filter(models.Certificate.id == cert_id).first()


def update_certificate(db: Session, cert_id: int, cert_update: schemas.CertificateUpdate):
    db_cert = db.query(models.Certificate).filter(models.Certificate.id == cert_id).first()
    if not db_cert:
        return None
    update_data = cert_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cert, key, value)
    db.commit()
    db.refresh(db_cert)
    return db_cert


def delete_certificate(db: Session, cert_id: int):
    db_cert = db.query(models.Certificate).filter(models.Certificate.id == cert_id).first()
    if not db_cert:
        return False
    db.delete(db_cert)
    db.commit()
    return True


# ---------- SEARCH ----------
def search_all(db: Session, query: str):
    search_term = f"%{query}%"
    
    projects = db.query(models.Project).filter(
        or_(
            models.Project.project_name.ilike(search_term),
            models.Project.techstack.ilike(search_term),
            models.Project.description.ilike(search_term),
        )
    ).all()
    
    dsa_topics = db.query(models.DSATopic).filter(
        or_(
            models.DSATopic.topic_name.ilike(search_term),
            models.DSATopic.category.ilike(search_term),
            models.DSATopic.description.ilike(search_term),
        )
    ).all()
    
    return {
        "projects": projects,
        "dsa_topics": dsa_topics
    }
