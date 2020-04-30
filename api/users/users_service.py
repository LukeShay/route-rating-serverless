from api.users.user import User
from api.users.users_repository import UsersRepository
from api.utils.auth import Jwt
from api.utils.regex import RegexUtils
from validate_email import validate_email
from typing import Optional, Dict, Tuple
import bcrypt
import logging
import uuid


SALT = bcrypt.gensalt(rounds=10, prefix=b"2a")


class UsersService:
    def __init__(self, database_session=None):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug("Initializing")
        self.users_repository = UsersRepository(database_session)
        self.jwt = Jwt()

    def login(self, user) -> Tuple[Optional[User], Optional[Dict]]:
        """
        Gets the user from the database an validates the passwords match.
        :param user: The user object. Must have username or email and password
        :return: The Tuple[Optional[User], Optional[Dict]]
        """
        self.log.debug(f"Attempting login:\n{user.as_camel_dict()}")

        user_result = self.get_user_by_email(user)

        if not user_result or not self.check_passwords(
            user.password, user_result.password
        ):
            return None, None

        jwt_token = self.jwt.generate_jwt_token(user_result)
        refresh_token = self.jwt.generate_refresh_token(user_result)

        return (
            user_result,
            {
                "Authorization": f"Bearer {jwt_token}",
                "Refresh": f"Bearer {refresh_token}",
            },
        )

    def get_user_by_username(self, request_user: User) -> Optional[User]:
        self.log.debug(f"Getting user by username:\n{request_user.as_camel_dict()}")

        result = self.users_repository.get_user_by_username(request_user.username)
        user = User.from_snake_dict(result.as_dict())
        result.free()

        return user if user.id and user.id != "" else None

    def get_user_by_email(self, request_user: User) -> Optional[User]:
        self.log.debug(f"Getting user by email:\n{request_user.as_camel_dict()}")

        result = self.users_repository.get_user_by_email(request_user.email)
        user = User.from_snake_dict(result.as_dict())
        result.free()

        return user if user.id and user.id != "" else None

    @staticmethod
    def check_passwords(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf8"), hashed_password.encode("utf8"))

    @staticmethod
    def encrypt_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf8"), SALT).decode("utf8")

    def create_user(self, new_user: User) -> User:
        new_user.id = str(uuid.uuid4())
        new_user.password = self.encrypt_password(new_user.password)

        result = self.users_repository.save(new_user)
        user = User.from_snake_dict(result.as_dict())
        result.free()

        return user

    @staticmethod
    def valid_email(user: User) -> bool:
        return RegexUtils.valid_email(user.email) and validate_email(
            user.email, verify=True
        )

    @staticmethod
    def valid_username(user: User) -> bool:
        return (
            not RegexUtils.special_character(user.username) and len(user.username) > 0
        )

    @staticmethod
    def valid_phone_number(user: User) -> bool:
        return (
            not RegexUtils.non_number(user.phone_number)
            and len(user.phone_number) == 10
        )

    @staticmethod
    def valid_password(user: User) -> bool:
        return (
            len(user.password) > 7
            and RegexUtils.special_character(user.password)
            and RegexUtils.number(user.password)
            and RegexUtils.uppercase(user.password)
            and RegexUtils.lowercase(user.password)
        )

    def get_user_by_id(self, user) -> Optional[User]:
        self.log.debug(f"Getting user by id:\n{user.as_camel_dict()}")

        result = self.users_repository.get_user_by_id(user.id)
        user = User.from_snake_dict(result.as_dict())
        result.free()

        return user if user.id and user.id != "" else None

    def update_user(self, user) -> Optional[User]:
        self.log.debug(f"Updating user:\n{user.as_camel_dict()}")

        result = self.users_repository.update(user.as_snake_dict())
        user = User.from_snake_dict(result.as_dict())
        result.free()

        return user if user.id and user.id != "" else None
