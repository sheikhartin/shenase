from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Request, Response, Body
from sqlalchemy.orm import Session

from shenase import schemas, crud, utils
from shenase.dependencies import get_db
from shenase.exceptions import (
    IncorrectUsernameOrPasswordError,
    CredentialsError,
)
from shenase.config import COOKIE_EXPIRE_DAYS

router = APIRouter()


@router.post('/login', response_model=schemas.User)
async def login(
    response: Response,
    login_form: schemas.LoginForm = Body(...),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_username(db=db, username=login_form.username)
    if user is None or not utils.verify_password(
        login_form.password, user.hashed_password
    ):
        raise IncorrectUsernameOrPasswordError
    response.set_cookie(
        key='user_id',
        value=str(user.id),
        expires=(
            datetime.now(timezone.utc) + timedelta(days=COOKIE_EXPIRE_DAYS)
        ),
        httponly=True,
        secure=True,
        samesite='lax',
    )
    return user


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key='user_id')
    return {'message': 'Successfully logged out.'}


@router.get('/users/me/', response_model=schemas.User)
async def read_users_me(request: Request):
    if request.state.user is None:
        raise CredentialsError
    return request.state.user
