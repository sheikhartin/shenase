from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from shenase import crud, utils
from shenase.dependencies import get_db


class SessionAuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        access_token = request.cookies.get('access_token')
        if access_token is not None:
            db = next(get_db())
            session = crud.validate_session(
                db=db,
                access_token=access_token,
                client_fingerprint=utils.generate_client_fingerprint(request),
            )
            if session is None:
                response = JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={
                        'detail': 'Invalid session. Please log in again.'
                    },
                )
                response.delete_cookie(key='access_token')
                return response
            request.state.user = crud.get_user_by_id(
                db=db, user_id=session.user_id
            )
        else:
            request.state.user = None
        return await call_next(request)
