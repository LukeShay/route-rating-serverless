import json


class User:
    def __init__(
        self,
        user_id,
        username,
        password,
        city,
        state,
        first_name,
        last_name,
        email,
        phone_number,
        authority,
        role,
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

    def all_fields_present(self):
        return self.id and self.new_user_fields_present()

    def new_user_fields_present(self):
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
    def from_snake_dict(cls, body):
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

    def as_camel_dict(self):
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

    def as_snake_dict(self):
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

    def as_dict(self):
        return self.as_camel_dict()

    def as_json_response(self):
        body = self.as_camel_dict()
        body.pop("password")
        return body
