from jwt import DecodeError
from munch import Munch
import jwt
import os
import logging
from api.utils.response_utils import ApiGatewayResponse
import traceback


ADMIN_AUTHORITY = "ADMIN"
BASIC_AUTHORITY = "BASIC"


class Auth:
    def __init__(self, event):
        self._event = Munch.fromDict(event)

    @property
    def auth_header(self) -> str:
        return (
            self.event.headers.Authorization[7:]
            if "Bearer " in self.event.headers.Authorization
            else self.event.headers.Authorization
        )

    @property
    def refresh_header(self) -> str:
        return (
            self.event.headers.Refresh[7:]
            if "Bearer " in self.event.headers.Refresh
            else self.event.headers.Refresh
        )

    def validate_jwt(self) -> bool:
        payload = self.get_jwt_payload()

        if not payload:
            logging.info("JWT payload is missing.")
            return False

        if not payload.get("username"):
            logging.info("username is missing from jwt payload.")
            return False

        if not payload.get("id"):
            logging.info("id is missing from jwt payload.")
            return False

        if not payload.get("authorities"):
            logging.info("authorities is missing from jwt payload.")
            return False

        if not payload.get("expires"):
            logging.info("expires is missing from jwt payload.")
            return False

        if not payload.get("issuedAt"):
            logging.info("expires is missing from jwt payload.")
            return False

        return True

    def is_admin(self):
        return ADMIN_AUTHORITY in self.get_jwt_payload().get("authorities")

    def get_jwt_payload(self) -> Munch or None:
        try:
            return Munch.fromDict(
                jwt.decode(
                    self.auth_header, self._jwt_secret, algorithms=[self.algorithm]
                )
            )
        except DecodeError as e:
            print(e)
            return None

    @property
    def _jwt_secret(self) -> str:
        return os.getenv("JWT_SECRET")

    @property
    def _refresh_secret(self) -> str:
        return os.getenv("REFRESH_SECRET")

    @property
    def algorithm(self):
        return "HS256"

    @property
    def event(self) -> Munch:
        return Munch.fromDict(self._event)


def basic_auth(function):
    def wrapper(*args, **kwargs):
        try:
            auth = Auth(args[0])

            if not auth.validate_jwt():
                return ApiGatewayResponse.forbidden_json_response()
        except Exception as e:
            logging.error("Exception raised while authenticating.")
            logging.error(traceback.format_exc())
            logging.exception(e)

            return ApiGatewayResponse.forbidden_json_response()

        return function(*args)

    return wrapper


def admin_auth(function):
    def wrapper(*args, **kwargs):
        try:
            auth = Auth(args[0])

            if not auth.validate_jwt():
                return ApiGatewayResponse.forbidden_json_response()

            if not auth.is_admin():
                return ApiGatewayResponse.unauthorized_json_response()
        except Exception as e:
            logging.error("Exception raised while authenticating.")
            logging.error(traceback.format_exc())
            logging.exception(e)

            return ApiGatewayResponse.forbidden_json_response()

        return function(*args)

    return wrapper
