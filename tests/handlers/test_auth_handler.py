from unittest import TestCase
from unittest.mock import patch
from api.auth import Auth
from api.handlers.auth_handler import (
    basic_auth_handler,
    admin_auth_handler,
    login_handler,
)
from api.users.user import User
from tests.utilities import (
    ApiGatewayEvent,
    generate_jwt,
    generate_refresh,
    DatabaseResult,
)
import os
import bcrypt


class TestAuthHandler(TestCase):
    def setUp(self) -> None:
        os.environ["TEST_RUN"] = "TRUE"

        self.valid_jwt_payload = {
            "email": "lukeshay",
            "id": "some_id",
            "authorities": "ADMIN",
            "expires_in": "never",
            "issued_at": "10000",
        }
        self.valid_basic_jwt_payload = {
            "email": "lukeshay",
            "id": "some_id",
            "authorities": "BASIC",
            "expires_in": "never",
            "issued_at": "10000",
        }
        self.invalid_jwt_payload_no_expires = {
            "email": "lukeshay",
            "id": "some_id",
            "authorities": "ADMIN",
            "issued_at": "10000",
        }
        self.invalid_jwt_payload_no_email = {
            "id": "some_id",
            "authorities": "ADMIN",
            "expires_in": "never",
            "issued_at": "10000",
        }
        self.invalid_jwt_payload_no_authorities = {
            "email": "lukeshay",
            "id": "some_id",
            "expires_in": "never",
            "issued_at": "10000",
        }
        self.invalid_jwt_payload_no_id = {
            "email": "lukeshay",
            "authorities": "ADMIN",
            "expires_in": "never",
            "issued_at": "10000",
        }
        self.invalid_jwt_payload_no_issued_at = {
            "email": "lukeshay",
            "id": "some_id",
            "authorities": "ADMIN",
            "expires_in": "never",
        }

        self.test_password = "some_password"
        self.test_id = "THIS IS AN ID"

        self.test_user = User(
            email="some_email",
            password=bcrypt.hashpw(
                self.test_password.encode("utf8"),
                bcrypt.gensalt(rounds=10, prefix=b"2a"),
            ).decode("utf8"),
            user_id=self.test_id,
            authority="ADMIN",
            role="ADMIN_ROLE",
            state="Iowa",
            city="Ames",
            username="some_username",
            first_name="some_first_name",
            last_name="some_last_name",
            phone_number="8765309",
        )

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

    def test_basic_invalid_jwt_no_email(self):
        response = basic_auth_handler(
            ApiGatewayEvent(
                headers={
                    "Authorization": generate_jwt(self.invalid_jwt_payload_no_email)
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

    def test_basic_invalid_jwt_no_issued_at(self):
        response = basic_auth_handler(
            ApiGatewayEvent(
                headers={
                    "Authorization": generate_jwt(self.invalid_jwt_payload_no_issued_at)
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

    def test_admin_invalid_jwt_no_email(self):
        response = admin_auth_handler(
            ApiGatewayEvent(
                headers={
                    "Authorization": generate_jwt(self.invalid_jwt_payload_no_email)
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

    def test_admin_invalid_jwt_no_issued_at(self):
        response = admin_auth_handler(
            ApiGatewayEvent(
                headers={
                    "Authorization": generate_jwt(self.invalid_jwt_payload_no_issued_at)
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

    @patch("api.users.users_repository.UsersRepository.get_user_by_email")
    def test_login_valid_credentials(self, mock_get_user_by_email):
        mock_get_user_by_email.return_value = DatabaseResult(self.test_user)

        response = login_handler(
            ApiGatewayEvent(
                body={"email": self.test_user.email, "password": self.test_password,}
            ).as_dict(),
            None,
        )

        self.assertEqual(200, response.get("statusCode", None))
        self.assertEqual(self.test_user.email, response.get("body")["email"])
        self.assertEqual(self.test_user.id, response.get("body")["id"])
        self.assertIsNotNone(response.get("headers").get("Authorization"))
        self.assertIsNotNone(response.get("headers").get("Refresh"))
        self.assertTrue("Bearer " in response.get("headers").get("Authorization"))
        self.assertTrue("Bearer " in response.get("headers").get("Refresh"))

    @patch("api.users.users_repository.UsersRepository.get_user_by_email")
    def test_login_invalid_credentials(self, mock_get_user_by_email):
        mock_get_user_by_email.return_value = DatabaseResult(self.test_user)

        response = login_handler(
            ApiGatewayEvent(
                body={"email": self.test_user.email, "password": "EYYYEYE",}
            ).as_dict(),
            None,
        )

        self.assertEqual(403, response.get("statusCode", None))
