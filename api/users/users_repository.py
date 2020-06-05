from api.users.user import User
from api.utils.db_utils import create_database_session
from typing import List


class UsersRepository:
    def __init__(self, database_session):
        self.table = (
            database_session if database_session else create_database_session()
        ).Table("users_table")

    def get_user_by_username(self, username) -> User:
        return User.from_snake_dict(self.table.get_item(Key={"username": username}))

    def get_users(self) -> List[User]:
        return [User.from_snake_dict(user) for user in self.table.scan()]

    def get_user_by_email(self, email) -> User:
        return User.from_snake_dict(self.table.get_item(Key={"email": email}))

    def get_user_by_id(self, user_id) -> User:
        return User.from_snake_dict(self.table.get_item(Key={"id": user_id}))

    def update(self, user) -> User:
        User.from_snake_dict(
            self.table.update_item(
                Key={
                    "id": user.id
                },
                ExpressionAttributeNames={
                    "#username": "username",
                    "#password": "password",
                    "#city": "city",
                    "#state": "state",
                    "#first_name": "first_name",
                    "#last_name": "last_name",
                    "#email": "email",
                    "#phone_number": "phone_number",
                    "#authority": "authority",
                    "#role": "role"
                },
                ExpressionAttributeValues=user.get_expression_attribute_values(),
                UpdateExpression="#username = :username, "
                                  "#password = :password, "
                                  "#city = :city, "
                                  "#state = :state, "
                                  "#first_name = :first_name, "
                                  "#last_name = :last_name, "
                                  "#email = :email, "
                                  "#phone_number = :phone_number, "
                                  "#authority = :authority, "
                                  "#role = :role",
                ReturnValues='ALL_NEW',
            )
        )
        return self.get_user_by_id(user.id)

    def save(self, user) -> User:
        self.table.put_item(user)
        return self.get_user_by_id(user.id)
