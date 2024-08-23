from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, EmailStr

from shenase import enums


class ProfileBase(BaseModel):
    display_name: str = Field(..., min_length=3, max_length=50)
    avatar: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=300)
    location: Optional[str] = Field(None, max_length=200)


class ProfileCreate(ProfileBase):
    pass


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


class Token(BaseModel):
    access_token: str
    token_type: str
