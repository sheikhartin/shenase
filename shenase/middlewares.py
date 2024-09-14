from fastapi import Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from shenase import crud
from shenase.dependencies import get_db
from shenase.exceptions import CredentialsError


class CookieAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        user_id = request.cookies.get('user_id')
        if user_id is not None:
            try:
                db = next(get_db())
                user = crud.get_user_by_id(db=db, user_id=user_id)
                if user is None:
                    raise CredentialsError
                request.state.user = user
            except Exception as e:
                raise CredentialsError from e
        else:
            request.state.user = None
        return await call_next(request)
