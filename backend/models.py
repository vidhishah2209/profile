from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from database import Base


class BasicInfo(Base):
    __tablename__ = "basic_info"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    location = Column(String(200))
    linkedin = Column(String(200))
    github = Column(String(200))
    leetcode = Column(String(200))
    bio = Column(Text)

    education = relationship("Education", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    dsa_topics = relationship("DSATopic", back_populates="user", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="user", cascade="all, delete-orphan")


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String(200), nullable=False)
    degree = Column(String(100))
    field_of_study = Column(String(100))
    start_year = Column(String(10))
    end_year = Column(String(10))
    grade = Column(String(50))
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("basic_info.id", ondelete="CASCADE"))

    user = relationship("BasicInfo", back_populates="education")

    __table_args__ = (
        Index("ix_education_institution", "institution"),
    )


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(100), nullable=False)
    techstack = Column(String(200))
    description = Column(Text)
    project_url = Column(String(300))
    user_id = Column(Integer, ForeignKey("basic_info.id", ondelete="CASCADE"))

    user = relationship("BasicInfo", back_populates="projects")

    __table_args__ = (
        Index("ix_project_techstack", "techstack"),
    )


class DSATopic(Base):
    """Data Structures and Algorithms topics with problems solved"""
    __tablename__ = "dsa_topic"

    id = Column(Integer, primary_key=True, index=True)
    topic_name = Column(String(100), nullable=False)
    category = Column(String(50))  # "Data Structure" or "Algorithm"
    description = Column(Text)
    problems_solved = Column(Text)  # Comma-separated list of problem names
    resources = Column(Text)
    user_id = Column(Integer, ForeignKey("basic_info.id", ondelete="CASCADE"))

    user = relationship("BasicInfo", back_populates="dsa_topics")

    __table_args__ = (
        Index("ix_dsa_topic_category", "category"),
    )


class Certificate(Base):
    """Certificates and achievements"""
    __tablename__ = "certificate"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    issuer = Column(String(100))
    issue_date = Column(String(20))
    credential_url = Column(String(300))
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("basic_info.id", ondelete="CASCADE"))

    user = relationship("BasicInfo", back_populates="certificates")


class AdminUser(Base):
    """Admin user for authentication"""
    __tablename__ = "admin_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    profile_id = Column(Integer, ForeignKey("basic_info.id", ondelete="SET NULL"), nullable=True)
    
    profile = relationship("BasicInfo", backref="admin_user")
