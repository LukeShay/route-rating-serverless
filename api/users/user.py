import json


class User:
    def __init__(
        self,
        user_id=None,
        username=None,
        password=None,
        city=None,
        state=None,
        first_name=None,
        last_name=None,
        email=None,
        phone_number=None,
        authority=None,
        role=None,
    ):
        self.id = user_id
        self.username = username
        self.password = password
        self.city = city
        self.state = state
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.authority = authority
        self.role = role

    def all_fields_present(self) -> bool:
        return self.id and self.new_user_fields_present()

    def new_user_fields_present(self) -> bool:
        return (
            self.username
            and self.password
            and self.city
            and self.state
            and self.first_name
            and self.last_name
            and self.email
            and self.phone_number
        )

    @classmethod
    def from_camel_dict(cls, body):
        if isinstance(body, str):
            body = json.loads(body)

        return cls(
            body.get("id", None),
            body.get("username", None),
            body.get("password", None),
            body.get("city", None),
            body.get("state", None),
            body.get("firstName", None),
            body.get("lastName", None),
            body.get("email", None),
            body.get("phoneNumber"),
            body.get("authority", None),
            body.get("role", None),
        )

    @classmethod
    def from_snake_dict(cls, body) -> User:
        if isinstance(body, str):
            body = json.loads(body)

        return cls(
            body.get("id", None),
            body.get("username", None),
            body.get("password", None),
            body.get("city", None),
            body.get("state", None),
            body.get("first_name", None),
            body.get("last_name", None),
            body.get("email", None),
            body.get("phone_number"),
            body.get("authority", None),
            body.get("role", None),
        )

    def as_camel_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "city": self.city,
            "state": self.state,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "phoneNumber": self.phone_number,
            "authority": self.authority,
            "role": self.role,
        }

    def as_snake_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "city": self.city,
            "state": self.state,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "authority": self.authority,
            "role": self.role,
        }

    def as_dict(self) -> dict:
        return self.as_camel_dict()

    def as_json_response(self):
        body = self.as_camel_dict()
        body.pop("password")
        return body

    def __add__(self, other):
        if not isinstance(other, User):
            raise TypeError

        user = User()

        user.first_name = self.first_name if self.first_name else other.first_name
        user.last_name = self.last_name if self.last_name else other.last_name
        user.id = self.id if self.id else other.id
        user.username = self.username if self.username else other.username
        user.password = self.password if self.password else other.password
        user.email = self.email if self.email else other.email
        user.city = self.city if self.city else other.city
        user.state = self.state if self.state else other.state
        user.phone_number = (
            self.phone_number if self.phone_number else other.phone_number
        )

        return user
