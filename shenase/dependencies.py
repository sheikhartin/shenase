from typing import Generator
from fastapi import Depends, Request
from sqlalchemy.orm import Session

from shenase import models, crud, enums
from shenase.database import SessionLocal
from shenase.exceptions import CredentialsError


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> models.User:
    user_id = request.cookies.get('user_id')
    if user_id is not None:
        user = crud.get_user_by_id(db, user_id=int(user_id))
        if user is None:
            raise CredentialsError
        return user
    raise CredentialsError


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if current_user.status != enums.UserStatus.ACTIVE:
        raise CredentialsError
    return current_user
