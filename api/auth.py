from jwt import DecodeError
from munch import Munch
import jwt
import os
import logging
import time


ADMIN_AUTHORITY = "ADMIN"
BASIC_AUTHORITY = "BASIC"


def current_milli_time():
    return int(round(time.time() * 1000))


class JwtPayload:
    def __init__(self, user_id, email, authorities, issued_at, expires_in):
        self.id = user_id
        self.email = email
        self.authorities = authorities
        self.issued_at = issued_at
        self.expires_in = expires_in

    @classmethod
    def from_jwt_payload(cls, jwt_payload):
        return cls(
            jwt_payload.get("id", None),
            jwt_payload.get("email", None),
            jwt_payload.get("authorities", None),
            jwt_payload.get("issued_at", None),
            jwt_payload.get("expires_in", None),
        )

    @classmethod
    def generate_as_dict(cls, user_id, email, authorities, expires_in):
        return cls(
            user_id, email, authorities, current_milli_time(), expires_in
        ).as_dict()

    def as_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "authorities": self.authorities,
            "issued_at": self.issued_at,
            "expires_in": self.expires_in,
        }


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

        if not payload.email:
            logging.info("username is missing from jwt payload.")
            return False

        if not payload.id:
            logging.info("id is missing from jwt payload.")
            return False

        if not payload.authorities:
            logging.info("authorities is missing from jwt payload.")
            return False

        if not payload.expires_in:
            logging.info("expires is missing from jwt payload.")
            return False

        if not payload.issued_at:
            logging.info("expires is missing from jwt payload.")
            return False

        return True

    def is_admin(self):
        return ADMIN_AUTHORITY in self.get_jwt_payload().authorities

    def get_jwt_payload(self) -> JwtPayload or None:
        try:
            return JwtPayload.from_jwt_payload(
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
