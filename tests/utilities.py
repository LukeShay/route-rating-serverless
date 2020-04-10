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
