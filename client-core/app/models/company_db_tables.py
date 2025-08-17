from typing import TYPE_CHECKING, List, Optional

from uuid import UUID
# from app.models.client_db_tables import Client
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.client_db_tables import Client

class Company(SQLModel, table=True):
    __tablename__ = "companies"
    __table_args__ = {"schema": "public"}
    company_id: Optional[UUID] = Field(default=None, primary_key=True)
    company_name: str = Field(index=True, max_length=100)
    company_email: str = Field(index=True, max_length=100)
    company_phone: Optional[str] = Field(default=None, max_length=15)
    company_address: Optional[str] = Field(default=None, max_length=255)
    created_at: Optional[str] = Field(default=None, index=True)
    updated_at: Optional[str] = Field(default=None, index=True)
    country: Optional[str] = Field(default=None, max_length=50)
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    bio: Optional[str] = None
    vision: Optional[str] = None
    about: Optional[str] = None

    # owner_id: int = Field( foreign_key="public.clients.client_id",)


    services: List["Service"] = Relationship(back_populates="companies")
    projects: List["Project"] = Relationship(back_populates="companies")
    blogs: List["Blog"] = Relationship(back_populates="companies")
    created_at: Optional[str] = Field(default=None, index=True)
    updated_at: Optional[str] = Field(default=None, index=True)

    # One-to-many reverse relation
    blogs: list["Blog"] = Relationship(back_populates="company")
    owner: Optional["Client"] = Relationship(back_populates="company")
    services: list["Service"] = Relationship(back_populates="company")
    projects: list["Project"] = Relationship(back_populates="company")
    chats: list["Chat"] = Relationship(back_populates="company")
    collaborations: list["Collaboration"] = Relationship(back_populates="company")

class Service(SQLModel, table=True):
    __tablename__ = "services"
    __table_args__ = {"schema": "public"}
    service_id:Optional[UUID] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    domain: Optional[str] = None
    company_id: Optional[UUID] = Field(foreign_key="public.companies.company_id")
    company: Optional[Company] = Relationship(back_populates="services")
    created_at: Optional[str] = Field(default=None, index=True)
    updated_at: Optional[str] = Field(default=None, index=True)


class Project(SQLModel, table=True):
    __tablename__ = "projects"
    __table_args__ = {"schema": "public"}
    project_id: Optional[UUID] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    image: Optional[str] = None
    description: Optional[str] = None
    domain: Optional[str] = None
    website_url: Optional[str] = None
    tools: Optional[str] = None
    created_at: Optional[str] = Field(default=None, index=True)
    updated_at: Optional[str] = Field(default=None, index=True)
    status: Optional[str] = Field(default="active", max_length=50)
    start_date: Optional[str] = Field(default=None)
    end_date: Optional[str] = Field(default=None)
    metrics: Optional[str] = None
    company_id: Optional[UUID] = Field(foreign_key="public.companies.company_id")
    company: Optional[Company] = Relationship(back_populates="projects")

class Blog(SQLModel, table=True):
    __tablename__ = "blogs"
    __table_args__ = {"schema": "public"}
    blog_id: Optional[UUID] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    description: Optional[str] = None
    image: Optional[str] = None
    content: str = Field(nullable=False)

    company_id: Optional[UUID] = Field(foreign_key="public.companies.company_id")
    company: Optional[Company] = Relationship(back_populates="blogs")
    created_at: Optional[str] = Field(default=None, index=True)
    updated_at: Optional[str] = Field(default=None, index=True)

class Chat(SQLModel, table=True):
    __tablename__ = "chats"
    __table_args__ = {"schema": "public"}
    chat_id: Optional[UUID] = Field(default=None, primary_key=True)
    chat_to: Optional[UUID] = Field(foreign_key="public.companies.company_id")
    chat_from:Optional[UUID] = Field(foreign_key="public.companies.company_id")
    chat_message: str = Field(nullable=False)
    chat_timestamp: Optional[str] = Field(default=None, index=True)
    chat_status: Optional[str] = Field(default="active", max_length=50)
    created_at: Optional[str] = Field(default=None, index=True)
    updated_at: Optional[str] = Field(default=None, index=True)
    company: Optional[Company] = Relationship(back_populates="chats")

class Notification(SQLModel, table=True):
    __tablename__ = "notifications"
    __table_args__ = {"schema": "public"}
    notification_id: Optional[UUID] = Field(default=None, primary_key=True)
    notification_type: str = Field(nullable=False, max_length=50)
    notification_message: str = Field(nullable=False)
    notification_status: Optional[str] = Field(default="unread", max_length=50)
    notification_from: Optional[UUID] = Field(foreign_key="public.companies.company_id")
    notification_to: Optional[UUID] = Field(foreign_key="public.companies.company_id")
    notification_timestamp: Optional[str] = Field(default=None, index=True)
    notification_read_at: Optional[str] = Field(default=None, index=True)
    notification_priority: Optional[str] = Field(default="normal", max_length=50)
    created_at: Optional[str] = Field(default=None, index=True)
    updated_at: Optional[str] = Field(default=None, index=True)

    company_id: Optional[UUID] = Field(foreign_key="public.companies.company_id")
    company: Optional[Company] = Relationship(back_populates="notifications")

class Collaboration(SQLModel, table=True):
    __tablename__ = "collaborations"
    __table_args__ = {"schema": "public"}
    collaboration_id: Optional[UUID] = Field(default=None, primary_key=True)
    collaboration_from: Optional[UUID] = Field(foreign_key="public.companies.company_id")
    collaboration_to: Optional[UUID] =Field(foreign_key="public.companies.company_id")
    collaboration_status: Optional[str] = Field(default="active", max_length=50)
    created_at: Optional[str] = Field(default=None, index=True)
    updated_at: Optional[str] = Field(default=None, index=True)
    company: Optional[Company] = Relationship(back_populates="collaborations")