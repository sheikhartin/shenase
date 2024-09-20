from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from shenase import crud
from shenase.dependencies import get_db


class CookieAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        user_id = request.cookies.get('user_id')
        if user_id is not None:
            db = next(get_db())
            user = crud.get_user_by_id(db=db, user_id=user_id)
            if user is None:
                response = JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={
                        'detail': (
                            'Invalid cookie found! Please login again '
                            'to continue using the service.'
                        )
                    },
                )
                response.delete_cookie(key='user_id')
                return response
            request.state.user = user
        else:
            request.state.user = None
        return await call_next(request)
