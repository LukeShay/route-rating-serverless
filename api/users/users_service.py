from api.users.user import User
from api.utils.auth import Jwt
from api.utils.regex import RegexUtils
from validate_email import validate_email
from typing import Optional, Dict, Tuple
import bcrypt
import uuid
from api.utils.decorators import log

SALT = bcrypt.gensalt(rounds=10, prefix=b"2a")


class UsersService:
    def __init__(self):
        self.jwt = Jwt()
        if not User.exists():
            User.create_table()

    # @log()
    def login(self, user) -> Tuple[Optional[User], Optional[Dict]]:
        """
        Gets the user from the database an validates the passwords match.
        :param user: The user object. Must have username or email and password
        :return: The Tuple[Optional[User], Optional[Dict]]
        """
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

    # @log()
    def get_user_by_email(self, request_user: User) -> Optional[User]:
        user_iterator = User.scan(User.user_id == request_user.user_id)

        if user_iterator.total_count == 0:
            return None

        user = user_iterator.next()

        return user if user and user.user_id and user.user_id != "" else None

    # @log()
    @staticmethod
    def check_passwords(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf8"), hashed_password.encode("utf8"))

    # @log()
    @staticmethod
    def encrypt_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf8"), SALT).decode("utf8")

    # @log()
    def create_user(self, new_user: User) -> Optional[User]:
        new_user.user_id = str(uuid.uuid4())
        new_user.password = self.encrypt_password(new_user.password)

        user = new_user.save()

        return user if user and user.user_id and user.user_id != "" else None

    # @log()
    @staticmethod
    def valid_email(user: User) -> bool:
        return RegexUtils.valid_email(user.email) and validate_email(
            user.email, verify=True
        )

    # @log()
    @staticmethod
    def valid_username(user: User) -> bool:
        return (
            not RegexUtils.special_character(user.username) and len(user.username) > 0
        )

    # @log()
    @staticmethod
    def valid_phone_number(user: User) -> bool:
        return (
            not RegexUtils.non_number(user.phone_number)
            and len(user.phone_number) == 10
        )

    # @log()
    @staticmethod
    def valid_password(user: User) -> bool:
        return (
            len(user.password) > 7
            and RegexUtils.special_character(user.password)
            and RegexUtils.number(user.password)
            and RegexUtils.uppercase(user.password)
            and RegexUtils.lowercase(user.password)
        )

    # @log()
    def get_user_by_id(self, request_user: User) -> Optional[User]:
        user_iterator = User.scan(User.user_id == request_user.user_id)

        if user_iterator.total_count == 0:
            return None

        user = user_iterator.next()

        return user if user and user.user_id and user.user_id != "" else None

    # @log()
    def update_user(self, updated_user: User) -> Optional[User]:
        user = updated_user.save()

        return user if user and user.user_id and user.user_id != "" else None
