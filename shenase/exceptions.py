from fastapi import HTTPException, status


class UserNotFoundError(HTTPException):
    def __init__(self, username: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with username `{username}` not found.',
        )


class InactiveUserError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Inactive user.',
        )


class UsernameAlreadyExistsError(HTTPException):
    def __init__(self, username: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Username `{username}` already registered.',
        )


class EmailAlreadyExistsError(HTTPException):
    def __init__(self, email: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Email `{email}` already registered.',
        )


class UserCreationError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Failed to create user.',
        )


class UserUpdateError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Failed to update user.',
        )


class NotAuthorizedError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized.',
        )


class IncorrectUsernameOrPasswordError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password.',
            headers={'WWW-Authenticate': 'Bearer'},
        )


class CredentialsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
