"""
Database Schemas

Pydantic models that define MongoDB collections used by the app.
Each class name maps to a collection with the lowercase name.
- Member -> "member"
- Post -> "post"
- Event -> "event"
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class Member(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    city: Optional[str] = Field(None, description="City or region")
    interests: Optional[List[str]] = Field(None, description="Topics of interest")

class Post(BaseModel):
    title: str = Field(..., description="Post title")
    summary: Optional[str] = Field(None, description="Short summary")
    body: Optional[str] = Field(None, description="Full content (optional)")
    image_url: Optional[str] = Field(None, description="Hero image URL")
    published_at: Optional[datetime] = Field(None, description="Publish timestamp")

class Event(BaseModel):
    name: str = Field(..., description="Event name")
    description: Optional[str] = Field(None, description="Event description")
    location: Optional[str] = Field(None, description="Location or online link")
    starts_at: Optional[datetime] = Field(None, description="Start time")
    ends_at: Optional[datetime] = Field(None, description="End time")
