from enum import StrEnum, auto


class UserRole(StrEnum):
    ADMIN = auto()
    MODERATOR = auto()
    USER = auto()


class UserStatus(StrEnum):
    ACTIVE = auto()
    INACTIVE = auto()
    SUSPENDED = auto()
