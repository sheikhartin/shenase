from typing import Generator
from fastapi import Depends, Request
from sqlalchemy.orm import Session

from shenase import models, enums
from shenase.database import SessionLocal
from shenase.exceptions import CredentialsError


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_access_token(request: Request) -> str:
    access_token = request.cookies.get('access_token')
    if access_token is None:
        raise CredentialsError
    return access_token


async def get_current_user(request: Request) -> models.User:
    user = request.state.user
    if user is None:
        raise CredentialsError
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if current_user.status != enums.UserStatus.ACTIVE:
        raise CredentialsError
    return current_user
