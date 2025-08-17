from typing import List, Optional
from pydantic import BaseModel, EmailStr


# -------------------
# Company Schemas
# -------------------

class CompanyBase(BaseModel):
    company_name: str
    company_email: str
    company_phone: Optional[str] = None
    company_address: Optional[str] = None
    country: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    bio: Optional[str] = None
    vision: Optional[str] = None
    about: Optional[str] = None

class CompanyCreate(CompanyBase):
    owner_id: int

class CompanyRead(CompanyBase):
    company_id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True


# -------------------
# Service Schemas
# -------------------

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    domain: Optional[str] = None
    company_id: int

class ServiceCreate(ServiceBase):
    pass

class ServiceRead(ServiceBase):
    service_id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True


# -------------------
# Project Schemas
# -------------------

class ProjectBase(BaseModel):
    title: str
    image: Optional[str] = None
    description: Optional[str] = None
    domain: Optional[str] = None
    website_url: Optional[str] = None
    tools: Optional[str] = None
    status: Optional[str] = "active"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    metrics: Optional[str] = None
    company_id: int

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    project_id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True


# -------------------
# Blog Schemas
# -------------------

class BlogBase(BaseModel):
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    content: str
    company_id: int

class BlogCreate(BlogBase):
    pass

class BlogRead(BlogBase):
    id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True


# -------------------
# Chat Schemas
# -------------------

class ChatBase(BaseModel):
    chat_to: Optional[str] = None
    chat_from: Optional[str] = None
    chat_message: str
    chat_timestamp: Optional[str] = None
    chat_status: Optional[str] = "active"

class ChatCreate(ChatBase):
    pass

class ChatRead(ChatBase):
    chat_id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True


# -------------------
# Notification Schemas
# -------------------

class NotificationBase(BaseModel):
    notification_type: str
    notification_message: str
    notification_status: Optional[str] = "unread"
    notification_from: Optional[str] = None
    notification_to: Optional[str] = None
    notification_timestamp: Optional[str] = None
    notification_read_at: Optional[str] = None
    notification_priority: Optional[str] = "normal"
    company_id: int

class NotificationCreate(NotificationBase):
    pass

class NotificationRead(NotificationBase):
    notification_id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True


# -------------------
# Collaboration Schemas
# -------------------

class CollaborationBase(BaseModel):
    collaboration_from: str
    collaboration_to: str
    collaboration_status: Optional[str] = "active"

class CollaborationCreate(CollaborationBase):
    pass

class CollaborationRead(CollaborationBase):
    collaboration_id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True
