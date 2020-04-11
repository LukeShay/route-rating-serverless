from api.utils.db_utils import create_database_session


class UsersRepository:
    def __init__(self, database_session):
        self.session = (
            database_session if database_session else create_database_session()
        )

    def get_user_by_username(self, username):
        return self.session.query(
            "SELECT * FROM users WHERE username=%(username)s LIMIT 1",
            {"username": username},
        )

    def get_users(self):
        return self.session.query("SELECT * FROM users")
