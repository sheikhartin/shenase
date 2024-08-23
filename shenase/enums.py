from enum import Enum, auto


class UserRole(Enum):
    ADMIN = auto()
    MODERATOR = auto()
    USER = auto()
