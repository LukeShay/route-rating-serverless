from unittest.mock import Mock

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

    return jwt.encode(payload, secret, algorithm="HS256").decode("utf8")


def generate_refresh(payload, secret=None):
    if not secret:
        secret = os.getenv("REFRESH_SECRET")

    return jwt.encode(payload, secret, algorithm="HS256").decode("utf8")


class DatabaseResult:
    def __init__(self, result):
        self.result = result

    def as_dict(self):
        return self.result.as_snake_dict() if self.result else {}

    def free(self):
        return


class MockUsersRepository:
    def __init__(self):
        self.get_user_by_email = Mock(return_value=DatabaseResult(None))
        self.get_user_by_username = Mock(return_value=DatabaseResult(None))
        self.get_user_by_id = Mock(return_value=DatabaseResult(None))
        self.update = Mock(return_value=DatabaseResult(None))
        self.save = Mock(return_value=DatabaseResult(None))
