from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from shenase import models, schemas, crud, utils
from shenase.database import get_db
from shenase.exceptions import (
    InactiveUserError,
    IncorrectUsernameOrPasswordError,
    CredentialsError,
)
from shenase.config import (
    JWT_ENCRYPTION_SECRET,
    JWT_SIGNATURE_METHOD,
    JWT_ACCESS_TOKEN_TTL_MINUTES,
)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict) -> str:
    return jwt.encode(
        {
            **data,
            'exp': (
                datetime.now(timezone.utc)
                + timedelta(minutes=JWT_ACCESS_TOKEN_TTL_MINUTES)
            ),
        },
        JWT_ENCRYPTION_SECRET,
        algorithm=JWT_SIGNATURE_METHOD,
    )


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> models.User:
    try:
        payload = jwt.decode(
            token,
            JWT_ENCRYPTION_SECRET,
            algorithms=[JWT_SIGNATURE_METHOD],
        )
        username = payload.get('sub')
        if username is None:
            raise CredentialsError
    except jwt.PyJWTError:
        raise CredentialsError

    user = crud.get_user_by_username(db=db, username=username)
    if user is None:
        raise CredentialsError
    return user


async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise InactiveUserError
    return current_user


@router.post('/token', response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_username(db=db, username=form_data.username)
    if not user or not utils.verify_password(
        form_data.password, user.hashed_password
    ):
        raise IncorrectUsernameOrPasswordError
    return {
        'access_token': create_access_token(data={'sub': user.username}),
        'token_type': 'bearer',
    }


@router.get('/users/me/', response_model=schemas.User)
async def read_users_me(
    current_user: schemas.User = Depends(get_current_active_user),
):
    return current_user
