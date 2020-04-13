from api.users.users_repository import UsersRepository
from api.users.user import User
import logging
import bcrypt


SALT = bcrypt.gensalt(rounds=10, prefix=b"2a")


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

        user_result = self.get_user_by_username(user)

        if not user_result.id or not UsersService.check_passwords(
            user.password, user_result.password
        ):
            return None

        return user_result

    def get_user_by_username(self, request_user: User) -> User or None:
        logging.debug(f"Getting user by username:\n{request_user.as_camel_dict()}")

        result = self.users_repository.get_user_by_username(request_user.username)

        user = User.from_snake_dict(result.as_dict())

        result.free()
        return user

    @staticmethod
    def check_passwords(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf8"), hashed_password.encode("utf8"))

    @staticmethod
    def encrypt_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf8"), SALT)
