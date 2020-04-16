import jwt
import os


class ApiGatewayEvent:
    def __init__(self, headers=None, body=None):
        self.headers = headers
        self.body = body

    def as_dict(self):
        return {"headers": self.headers, "body": self.body}


def generate_jwt(payload, secret=None):
    if not secret:
        secret = os.getenv("JWT_SECRET")

    return jwt.encode(payload, secret, algorithm="HS256").decode("UTF-8")


def generate_refresh(payload, secret=None):
    if not secret:
        secret = os.getenv("REFRESH_SECRET")

    return jwt.encode(payload, secret, algorithm="HS256").decode("UTF-8")


class DatabaseResult:
    def __init__(self, result):
        self.result = result

    def as_dict(self):
        return self.result.as_snake_dict() if self.result else {}

    def free(self):
        return
