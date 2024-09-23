from fastapi import APIRouter, Depends, Request, Response, Body
from sqlalchemy.orm import Session

from shenase import schemas, crud, utils
from shenase.dependencies import get_db, get_access_token
from shenase.exceptions import (
    IncorrectUsernameOrPasswordError,
    CredentialsError,
)

router = APIRouter()


@router.post('/login/', response_model=schemas.User)
async def login(
    request: Request,
    response: Response,
    username: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_username(db=db, username=username)
    if user is None or not utils.verify_password(
        password, user.hashed_password
    ):
        raise IncorrectUsernameOrPasswordError

    session = crud.create_session(
        db=db,
        user_id=user.id,
        client_fingerprint=utils.generate_client_fingerprint(request),
    )
    response.set_cookie(
        key='access_token',
        value=session.access_token,
        httponly=True,
        secure=True,
        samesite='lax',
    )
    return user


@router.post('/logout/')
async def logout(
    response: Response,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    crud.deactivate_session(db=db, access_token=access_token)
    response.delete_cookie(key='access_token')
    return {'message': 'Successfully logged out.'}


@router.get('/users/me/', response_model=schemas.User)
async def read_users_me(request: Request):
    if request.state.user is None:
        raise CredentialsError
    return request.state.user
