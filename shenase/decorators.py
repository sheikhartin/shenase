from functools import wraps
from typing import Callable, Any, Awaitable

from shenase import enums
from shenase.exceptions import NotAuthorizedError


def role_required(
    roles: list[enums.UserRole],
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    def decorator(
        func: Callable[..., Awaitable[Any]],
    ) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_user = kwargs.get('current_user')
            if current_user is None:
                raise RuntimeError
            elif current_user.role not in roles:
                raise NotAuthorizedError
            return await func(*args, **kwargs)

        return wrapper

    return decorator
