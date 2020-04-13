from api.users.users_repository import UsersRepository
from api.users.user import User
import logging
import bcrypt
import os
import jwt
from api.auth import JwtPayload


SALT = bcrypt.gensalt(rounds=10, prefix=b"2a")

ONE_DAY = 86_400_000
ONE_WEEK = ONE_DAY * 7


class UsersService:
    def __init__(self, database_session):
        logging.debug("Initializing UsersService")
        self.users_repository = UsersRepository(database_session)

    def login(self, user) -> User or None:
        """
        Gets the user from the database an validates the passwords match.
        :param user: The user object. Must have username or email and password
        :return: The user or none
        """
        logging.debug(f"Attempting login:\n{user.as_camel_dict()}")

        user_result = self.get_user_by_email(user)

        if not user_result.all_fields_present() or not UsersService.check_passwords(
            user.password, user_result.password
        ):
            return None, None

        jwt_token = self.generate_jwt_token(user_result)
        refresh_token = self.generate_refresh_token(user_result)

        return (
            user_result,
            {
                "Authorization": f"Bearer {jwt_token}",
                "Refresh": f"Bearer {refresh_token}",
            },
        )

    # def get_user_by_username(self, request_user: User) -> User or None:
    #     logging.debug(f"Getting user by username:\n{request_user.as_camel_dict()}")
    #
    #     result = self.users_repository.get_user_by_username(request_user.username)
    #
    #     user = User.from_snake_dict(result.as_dict())
    #
    #     result.free()
    #     return user

    def get_user_by_email(self, request_user: User) -> User or None:
        logging.debug(f"Getting user by email:\n{request_user.as_camel_dict()}")

        result = self.users_repository.get_user_by_email(request_user.email)

        user = User.from_snake_dict(result.as_dict())

        logging.debug(f"User from database:\n{user.as_camel_dict()}")

        result.free()
        return user

    def generate_jwt_token(self, user):
        return self._generate_jwt(
            JwtPayload.generate_as_dict(user.id, user.email, [user.authority], ONE_DAY),
            self._jwt_secret,
        )

    def generate_refresh_token(self, user):
        return self._generate_jwt(
            JwtPayload.generate_as_dict(
                user.id, user.email, [user.authority], ONE_WEEK
            ),
            self._refresh_secret,
        )

    def _generate_jwt(self, payload, secret):
        return jwt.encode(payload, secret, self._algorithm)

    @property
    def _jwt_secret(self) -> str:
        return os.getenv("JWT_SECRET")

    @property
    def _refresh_secret(self) -> str:
        return os.getenv("REFRESH_SECRET")

    @property
    def _algorithm(self):
        return "HS256"

    @staticmethod
    def check_passwords(password: str, hashed_password: str) -> bool:
        logging.debug("Comparing passwords")
        return bcrypt.checkpw(password.encode("utf8"), hashed_password.encode("utf8"))

    @staticmethod
    def encrypt_password(password: str) -> str:
        logging.debug("Encrypting password")
        return bcrypt.hashpw(password.encode("utf8"), SALT)
