from typing import TYPE_CHECKING, List, Optional
from uuid import UUID
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.company_db_tables import Company

class Client(SQLModel, table=True):
    __tablename__ = "clients"
    __table_args__ = {"schema": "public"}
    client_id: Optional[UUID] = Field(default=None, primary_key=True)
    client_name: str = Field(index=True, max_length=100)
    client_username: str = Field(index=True, max_length=100)
    client_email: str = Field(index=True, max_length=100)
    client_phone: Optional[str] = Field(default=None, max_length=15)
    client_address: Optional[str] = Field(default=None, max_length=255)
    role: str = Field(default="user", max_length=50)
    client_role_in_company: Optional[str] = Field(default=None, max_length=50)
    created_at: Optional[str] = Field(default=None, index=True)
    updated_at: Optional[str] = Field(default=None, index=True)
    country: Optional[str] = Field(default=None, max_length=50)
    hashed_password: str = Field(nullable=False)
    company_id: Optional[UUID] = Field( foreign_key="public.companies.company_id")

    company: Optional["Company"] = Relationship(back_populates="owner")