from typing import Optional

from fastapi import APIRouter, Depends, Body, UploadFile, File
from sqlalchemy.orm import Session

from shenase import schemas, crud, enums
from shenase.database import get_db
from shenase.decorators import role_required
from shenase.exceptions import UserCreationError, UserUpdateError
from shenase.routers.auth import get_current_active_user

router = APIRouter()


@router.get('/users/', response_model=list[schemas.User])
@role_required([enums.UserRole.ADMIN])
async def read_users(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    return crud.get_users(db=db)


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
            avatar=avatar,
        )
    except ValueError as e:
        raise UserCreationError from e
    return crud.create_user(db=db, user=new_user)


@router.put('/users/me/', response_model=schemas.User)
async def update_user(
    username: str = Body(None),
    email: str = Body(None),
    password: str = Body(None),
    display_name: str = Body(None),
    bio: Optional[str] = Body(None),
    location: Optional[str] = Body(None),
    avatar: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    try:
        user_data = schemas.UserProfileUpdate(
            username=username,
            email=email,
            password=password,
            display_name=display_name,
            bio=bio,
            location=location,
            avatar=avatar,
        )
    except ValueError as e:
        raise UserUpdateError from e
    return crud.update_user(db=db, user=user_data, current_user=current_user)


@router.put('/users/{username}/role/', response_model=schemas.User)
@role_required([enums.UserRole.ADMIN])
async def change_user_role(
    username: str,
    new_role: enums.UserRole,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    return crud.update_user_role(db=db, username=username, new_role=new_role)
