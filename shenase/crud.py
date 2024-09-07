import os
import shutil
import uuid
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from shenase import models, schemas, enums, utils
from shenase.exceptions import (
    UserNotFoundError,
    UsernameAlreadyExistsError,
    EmailAlreadyExistsError,
)
from shenase.config import AVATAR_STORAGE_PATH


def get_users(db: Session) -> Optional[list[models.User]]:
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
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
        save_avatar(db, db_user.id, user.avatar)
        if user.avatar is not None
        else None
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


def update_user(
    db: Session,
    user: schemas.UserProfileUpdate,
    current_user: models.User,
) -> models.User:
    if (
        user.username is not None
        and get_user_by_username(db, user.username) is not None
    ):
        raise UsernameAlreadyExistsError(user.username)
    elif (
        user.email is not None
        and get_user_by_email(db, user.email) is not None
    ):
        raise EmailAlreadyExistsError(user.email)

    current_user.username = user.username or current_user.username
    current_user.email = user.email or current_user.email
    if user.password is not None:
        current_user.password = utils.get_password_hash(user.password)
    current_user.profile.display_name = (
        user.display_name or current_user.profile.display_name
    )
    current_user.profile.bio = user.bio or current_user.profile.bio
    current_user.profile.location = (
        user.location or current_user.profile.location
    )
    if user.avatar is not None:
        avatar_file_path = save_avatar(db, current_user.id, user.avatar)
        current_user.profile.avatar = avatar_file_path

    db.commit()
    db.refresh(current_user)
    return current_user


def update_user_role(
    db: Session,
    username: str,
    new_role: enums.UserRole,
) -> models.User:
    db_user = get_user_by_username(db, username)
    if db_user is None:
        raise UserNotFoundError(username)

    db_user.role = new_role
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_status(
    db: Session,
    username: str,
    new_status: enums.UserStatus,
) -> models.User:
    db_user = get_user_by_username(db, username)
    if db_user is None:
        raise UserNotFoundError(username)

    db_user.status = new_status
    db.commit()
    db.refresh(db_user)
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
