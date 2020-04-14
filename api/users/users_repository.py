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

    def get_user_by_email(self, email):
        return self.session.query(
            "SELECT * FROM users WHERE email=%(email)s LIMIT 1", {"email": email}
        )

    def get_user_by_id(self, user_id):
        return self.session.query(
            "SELECT * FROM users WHERE id=%(id)s LIMIT 1", {"id": str(user_id)}
        )

    def save(self, user):
        self.session.query(
            "INSERT INTO USERS ("
            "id, "
            "first_name, "
            "last_name, "
            "email, "
            "username, "
            "password, "
            "phone_number, "
            "city, state, "
            "authority, "
            "role, "
            "country) "
            "VALUES ("
            "%(id)s, "
            "%(first_name)s, "
            "%(last_name)s, "
            "%(email)s, "
            "%(username)s, "
            "%(password)s, "
            "%(phone_number)s, "
            "%(city)s, "
            "%(state)s, "
            "%(authority)s, "
            "%(role)s, "
            "'United States')",
            user.as_snake_dict(),
        )
        return self.get_user_by_id(user.id)
