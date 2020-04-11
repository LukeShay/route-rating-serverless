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

    @classmethod
    def from_camel_dict(cls, json):
        return cls(
            json.get("id", None),
            json.get("username", None),
            json.get("password", None),
            json.get("city", None),
            json.get("state", None),
            json.get("firstName", None),
            json.get("lastName", None),
            json.get("email", None),
            json.get("phoneNumber"),
            json.get("authority", None),
            json.get("role", None),
        )

    @classmethod
    def from_snake_dict(cls, json):
        return cls(
            json.get("id", None),
            json.get("username", None),
            json.get("password", None),
            json.get("city", None),
            json.get("state", None),
            json.get("first_name", None),
            json.get("last_name", None),
            json.get("email", None),
            json.get("phone_number"),
            json.get("authority", None),
            json.get("role", None),
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

    def as_dict(self):
        return self.as_camel_dict()

    def as_json_response(self):
        body = self.as_camel_dict()
        body.pop("password")
        return body
