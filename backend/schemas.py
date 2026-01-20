from pydantic import BaseModel, ConfigDict
from typing import List, Optional


# -------- Education --------
class EducationBase(BaseModel):
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_year: Optional[str] = None
    end_year: Optional[str] = None
    grade: Optional[str] = None
    description: Optional[str] = None


class EducationCreate(EducationBase):
    user_id: int


class EducationUpdate(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_year: Optional[str] = None
    end_year: Optional[str] = None
    grade: Optional[str] = None
    description: Optional[str] = None


class EducationOut(EducationBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# -------- Project --------
class ProjectBase(BaseModel):
    project_name: str
    techstack: Optional[str] = None
    description: Optional[str] = None
    project_url: Optional[str] = None


class ProjectCreate(ProjectBase):
    user_id: int


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    techstack: Optional[str] = None
    description: Optional[str] = None
    project_url: Optional[str] = None


class ProjectOut(ProjectBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# -------- DSA Topic --------
class DSATopicBase(BaseModel):
    topic_name: str
    category: Optional[str] = None  # "Data Structure" or "Algorithm"
    description: Optional[str] = None
    problems_solved: Optional[str] = None  # Comma-separated problem names
    resources: Optional[str] = None


class DSATopicCreate(DSATopicBase):
    user_id: int


class DSATopicUpdate(BaseModel):
    topic_name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    problems_solved: Optional[str] = None
    resources: Optional[str] = None


class DSATopicOut(DSATopicBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# -------- Certificate --------
class CertificateBase(BaseModel):
    title: str
    issuer: Optional[str] = None
    issue_date: Optional[str] = None
    credential_url: Optional[str] = None
    description: Optional[str] = None


class CertificateCreate(CertificateBase):
    user_id: int


class CertificateUpdate(BaseModel):
    title: Optional[str] = None
    issuer: Optional[str] = None
    issue_date: Optional[str] = None
    credential_url: Optional[str] = None
    description: Optional[str] = None


class CertificateOut(CertificateBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# -------- Basic Info --------
class BasicInfoBase(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    leetcode: Optional[str] = None
    bio: Optional[str] = None


class BasicInfoCreate(BasicInfoBase):
    pass


class BasicInfoUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    leetcode: Optional[str] = None
    bio: Optional[str] = None


class BasicInfoOut(BasicInfoBase):
    id: int
    education: List[EducationOut] = []
    projects: List[ProjectOut] = []
    dsa_topics: List[DSATopicOut] = []
    certificates: List[CertificateOut] = []

    model_config = ConfigDict(from_attributes=True)


# -------- Auth --------
class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str
    profile_id: int | None = None

    model_config = ConfigDict(from_attributes=True)
