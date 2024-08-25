from typing import Optional

from fastapi import APIRouter, Depends, Body, UploadFile, File
from sqlalchemy.orm import Session

from shenase import schemas, crud
from shenase.database import get_db
from shenase.exceptions import UserCreationError
from shenase.routers.auth import get_current_active_user

router = APIRouter()


@router.post('/users/', response_model=schemas.User)
async def create_user(
    username: str = Body(...),
    email: str = Body(...),
    password: str = Body(...),
    display_name: str = Body(...),
    bio: Optional[str] = Body(None),
    location: Optional[str] = Body(None),
    avatar: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    try:
        new_user = schemas.UserCreate(
            username=username,
            email=email,
            password=password,
            display_name=display_name,
            bio=bio,
            location=location,
        )
    except ValueError as e:
        raise UserCreationError from e
    return crud.create_user(db=db, user=new_user, avatar=avatar)


@router.post('/users/avatar/', response_model=schemas.AvatarUploadResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    avatar_file_path = crud.save_avatar(
        db=db, user_id=current_user.id, file=file
    )
    return {
        'response_message': 'Avatar uploaded successfully.',
        'file_location': avatar_file_path,
    }
