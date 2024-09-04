from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, Field, EmailStr

from shenase import enums


class ProfileBase(BaseModel):
    display_name: str = Field(..., min_length=3, max_length=50)
    avatar: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=300)
    location: Optional[str] = Field(None, max_length=200)


class ProfileCreate(ProfileBase):
    avatar: Optional[UploadFile] = None


class Profile(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=35)
    email: EmailStr


class UserCreate(UserBase, ProfileCreate):
    password: str = Field(..., min_length=8, max_length=65)


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: enums.UserRole
    is_verified: bool
    is_active: bool
    created_at: datetime
    profile: Optional[Profile] = None


class AvatarUploadResponse(BaseModel):
    response_message: str
    file_location: str


class UserProfileUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=35)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=65)
    display_name: Optional[str] = Field(None, min_length=3, max_length=50)
    bio: Optional[str] = Field(None, max_length=300)
    location: Optional[str] = Field(None, max_length=200)
    avatar: Optional[UploadFile] = None


class Token(BaseModel):
    access_token: str
    token_type: str
