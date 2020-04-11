from unittest import TestCase

from api.auth import Auth
from api.handlers.auth_handler import basic_auth_handler, admin_auth_handler
from tests.utilities import ApiGatewayEvent, generate_jwt, generate_refresh
import os


class TestAuthHandler(TestCase):
    def setUp(self) -> None:
        self.valid_jwt_payload = {
            "username": "lukeshay",
            "id": "some_id",
            "authorities": "ADMIN",
            "expires": "never",
            "issuedAt": "10000",
        }
        self.valid_basic_jwt_payload = {
            "username": "lukeshay",
            "id": "some_id",
            "authorities": "BASIC",
            "expires": "never",
            "issuedAt": "10000",
        }
        self.invalid_jwt_payload_no_expires = {
            "username": "lukeshay",
            "id": "some_id",
            "authorities": "ADMIN",
        }
        self.invalid_jwt_payload_no_username = {
            "id": "some_id",
            "authorities": "ADMIN",
            "expires": "never",
        }
        self.invalid_jwt_payload_no_authorities = {
            "username": "lukeshay",
            "id": "some_id",
            "expires": "never",
        }
        self.invalid_jwt_payload_no_id = {
            "username": "lukeshay",
            "authorities": "ADMIN",
            "expires": "never",
        }
        self.invalid_jwt_payload_no_issuedAt = {
            "username": "lukeshay",
            "id": "some_id",
            "authorities": "ADMIN",
            "expires": "never",
        }

    def test_basic_admin_valid_jwt(self):
        response = basic_auth_handler(
            ApiGatewayEvent(
                headers={"Authorization": generate_jwt(self.valid_jwt_payload)}
            ).as_dict(),
            None,
        )

        self.assertEqual(200, response.get("statusCode", None))

    def test_basic_basic_valid_jwt(self):
        response = basic_auth_handler(
            ApiGatewayEvent(
                headers={"Authorization": generate_jwt(self.valid_basic_jwt_payload)}
            ).as_dict(),
            None,
        )

        self.assertEqual(200, response.get("statusCode", None))

    def test_basic_invalid_jwt_no_expires(self):
        response = basic_auth_handler(
            ApiGatewayEvent(
                headers={
                    "Authorization": generate_jwt(self.invalid_jwt_payload_no_expires)
                }
            ).as_dict(),
            None,
        )

        self.assertEqual(403, response.get("statusCode", None))

    def test_basic_invalid_jwt_no_username(self):
        response = basic_auth_handler(
            ApiGatewayEvent(
                headers={
                    "Authorization": generate_jwt(self.invalid_jwt_payload_no_username)
                }
            ).as_dict(),
            None,
        )

        self.assertEqual(403, response.get("statusCode", None))

    def test_basic_invalid_jwt_no_id(self):
        response = basic_auth_handler(
            ApiGatewayEvent(
                headers={"Authorization": generate_jwt(self.invalid_jwt_payload_no_id)}
            ).as_dict(),
            None,
        )

        self.assertEqual(403, response.get("statusCode", None))

    def test_basic_invalid_jwt_no_authorities(self):
        response = basic_auth_handler(
            ApiGatewayEvent(
                headers={
                    "Authorization": generate_jwt(
                        self.invalid_jwt_payload_no_authorities
                    )
                }
            ).as_dict(),
            None,
        )

        self.assertEqual(403, response.get("statusCode", None))

    def test_basic_invalid_jwt_no_issuedAt(self):
        response = basic_auth_handler(
            ApiGatewayEvent(
                headers={
                    "Authorization": generate_jwt(self.invalid_jwt_payload_no_issuedAt)
                }
            ).as_dict(),
            None,
        )

        self.assertEqual(403, response.get("statusCode", None))

    def test_basic_invalid_jwt_wrong_secret(self):
        response = basic_auth_handler(
            ApiGatewayEvent(
                headers={
                    "Authorization": generate_jwt(
                        self.valid_jwt_payload,
                        secret="nmSRM5ERGOE4NR8RE41cdvDeIUecHCjSiRzqztG2Fi1kOqol",
                    )
                }
            ).as_dict(),
            None,
        )

        self.assertEqual(403, response.get("statusCode", None))

    def test_basic_unexpected_exception(self):
        response = basic_auth_handler(ApiGatewayEvent().as_dict(), None)

        self.assertEqual(403, response.get("statusCode", None))

    def test_admin_admin_valid_jwt(self):
        response = admin_auth_handler(
            ApiGatewayEvent(
                headers={"Authorization": generate_jwt(self.valid_jwt_payload)}
            ).as_dict(),
            None,
        )

        self.assertEqual(200, response.get("statusCode", None))

    def test_admin_basic_valid_jwt(self):
        response = admin_auth_handler(
            ApiGatewayEvent(
                headers={"Authorization": generate_jwt(self.valid_basic_jwt_payload)}
            ).as_dict(),
            None,
        )

        self.assertEqual(401, response.get("statusCode", None))

    def test_admin_invalid_jwt_no_expires(self):
        response = admin_auth_handler(
            ApiGatewayEvent(
                headers={
                    "Authorization": generate_jwt(self.invalid_jwt_payload_no_expires)
                }
            ).as_dict(),
            None,
        )

        self.assertEqual(403, response.get("statusCode", None))

    def test_admin_invalid_jwt_no_username(self):
        response = admin_auth_handler(
            ApiGatewayEvent(
                headers={
                    "Authorization": generate_jwt(self.invalid_jwt_payload_no_username)
                }
            ).as_dict(),
            None,
        )

        self.assertEqual(403, response.get("statusCode", None))

    def test_admin_invalid_jwt_no_id(self):
        response = admin_auth_handler(
            ApiGatewayEvent(
                headers={"Authorization": generate_jwt(self.invalid_jwt_payload_no_id)}
            ).as_dict(),
            None,
        )

        self.assertEqual(403, response.get("statusCode", None))

    def test_admin_invalid_jwt_no_authorities(self):
        response = admin_auth_handler(
            ApiGatewayEvent(
                headers={
                    "Authorization": generate_jwt(
                        self.invalid_jwt_payload_no_authorities
                    )
                }
            ).as_dict(),
            None,
        )

        self.assertEqual(403, response.get("statusCode", None))

    def test_admin_invalid_jwt_no_issuedAt(self):
        response = admin_auth_handler(
            ApiGatewayEvent(
                headers={
                    "Authorization": generate_jwt(self.invalid_jwt_payload_no_issuedAt)
                }
            ).as_dict(),
            None,
        )

        self.assertEqual(403, response.get("statusCode", None))

    def test_admin_invalid_jwt_wrong_secret(self):
        response = admin_auth_handler(
            ApiGatewayEvent(
                headers={
                    "Authorization": generate_jwt(
                        self.valid_jwt_payload,
                        secret="nmSRM5ERGOE4NR8RE41cdvDeIUecHCjSiRzqztG2Fi1kOqol",
                    )
                }
            ).as_dict(),
            None,
        )

        self.assertEqual(403, response.get("statusCode", None))

    def test_admin_unexpected_exception(self):
        response = admin_auth_handler(ApiGatewayEvent().as_dict(), None)

        self.assertEqual(403, response.get("statusCode", None))

    def test_get_refresh_token(self):
        auth = Auth(
            ApiGatewayEvent(
                headers={
                    "Refresh": f"Bearer {generate_refresh(self.valid_jwt_payload)}"
                }
            ).as_dict(),
        )

        self.assertEqual(generate_refresh(self.valid_jwt_payload), auth.refresh_header)
        self.assertEqual(os.getenv("REFRESH_SECRET"), auth._refresh_secret)
