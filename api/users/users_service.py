from api.users.users_repository import UsersRepository
from api.users.user import User
import logging
import bcrypt
from api.auth import Jwt
import uuid
from api.utils.regex import RegexUtils
from validate_email import validate_email


SALT = bcrypt.gensalt(rounds=10, prefix=b"2a")


class UsersService:
    def __init__(self, database_session):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug("Initializing UsersService")
        self.users_repository = UsersRepository(database_session)
        self.jwt = Jwt()

    def login(self, user) -> User or None:
        """
        Gets the user from the database an validates the passwords match.
        :param user: The user object. Must have username or email and password
        :return: The user or none
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

    def get_user_by_username(self, request_user: User) -> User or None:
        self.log.debug(f"Getting user by username:\n{request_user.as_camel_dict()}")

        result = self.users_repository.get_user_by_username(request_user.username)

        user = User.from_snake_dict(result.as_dict())

        result.free()
        return user if user.id and user.id != "" else None

    def get_user_by_email(self, request_user: User) -> User or None:
        self.log.debug(f"Getting user by email:\n{request_user.as_camel_dict()}")

        result = self.users_repository.get_user_by_email(request_user.email)

        user = User.from_snake_dict(result.as_dict())

        self.log.debug(f"User from database:\n{user.as_camel_dict()}")

        result.free()

        return user if user.id and user.id != "" else None

    def check_passwords(self, password: str, hashed_password: str) -> bool:
        self.log.debug("Comparing passwords")
        return bcrypt.checkpw(password.encode("utf8"), hashed_password.encode("utf8"))

    def encrypt_password(self, password: str) -> bytes:
        self.log.debug("Encrypting password")
        return bcrypt.hashpw(password.encode("utf8"), SALT)

    def create_user(self, new_user: User) -> User:
        new_user.id = str(uuid.uuid4())
        new_user.password = self.encrypt_password(new_user.password).decode("utf8")

        result = self.users_repository.save(new_user)

        user = User.from_snake_dict(result.as_dict())

        result.free()

        return user

    def valid_email(self, user: User) -> bool:
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
