import os
import shutil
import uuid
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from shenase import models, schemas, utils
from shenase.exceptions import (
    UsernameAlreadyExistsError,
    EmailAlreadyExistsError,
)
from shenase.config import AVATAR_STORAGE_PATH


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return (
        db.query(models.User).filter(models.User.username == username).first()
    )


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_profile(db: Session, profile_id: int) -> Optional[models.Profile]:
    return (
        db.query(models.Profile)
        .filter(models.Profile.id == profile_id)
        .first()
    )


def get_profile_by_user_id(
    db: Session, user_id: int
) -> Optional[models.Profile]:
    return (
        db.query(models.Profile)
        .filter(models.Profile.user_id == user_id)
        .first()
    )


def create_user(
    db: Session,
    user: schemas.UserCreate,
    avatar: Optional[UploadFile] = None,
) -> models.User:
    if get_user_by_username(db, user.username) is not None:
        raise UsernameAlreadyExistsError(user.username)
    elif get_user_by_email(db, user.email) is not None:
        raise EmailAlreadyExistsError(user.email)

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=utils.get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    avatar_file_path = (
        save_avatar(db, db_user.id, avatar) if avatar is not None else None
    )
    db_profile = models.Profile(
        user_id=db_user.id,
        display_name=user.display_name,
        avatar=avatar_file_path,
        bio=user.bio,
        location=user.location,
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return db_user


def _create_unique_filename(filename: str) -> str:
    unique_id = uuid.uuid4().hex[:15]
    _, file_extension = os.path.splitext(filename)
    return f'{unique_id}{file_extension}'


def save_avatar(db: Session, user_id: int, file: UploadFile) -> str:
    filename = _create_unique_filename(file.filename)
    file_path = os.path.join(AVATAR_STORAGE_PATH, filename)
    with open(file_path, 'wb') as f:
        shutil.copyfileobj(file.file, f)

    db_profile = get_profile_by_user_id(db, user_id)
    if db_profile is not None:
        db_profile.avatar = filename
        db.commit()
        db.refresh(db_profile)

    return filename
