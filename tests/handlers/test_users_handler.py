import json
import uuid
from unittest import TestCase
from unittest.mock import patch, Mock

from api.users.user import User
from api.handlers.users_handler import create_user_handler, create_admin_user_handler
from api.users import users_service
from tests.offline_handler import OfflineHandler
from tests.test_base import TestBase

from tests.utilities import (
    ApiGatewayEvent,
    DatabaseResult,
    generate_jwt,
)


class TestUsersHandler(TestBase):
    def setUp(self) -> None:
        self.valid_new_user = User(
            first_name="first",
            last_name="last",
            email="email@gmail.com",
            password="LKJ)(*098ljk",
            username="someusername",
            city="Ames",
            state="Iowa",
            phone_number="9999999999",
            authority=None,
            role=None,
            user_id=None,
        )

        self.invalid_new_user = User(
            first_name="first",
            last_name="last",
            email="emailgmail.com",
            password="aa)(*098ljk",
            username="someu)(*&^%$sername",
            city="Ames",
            state="Iowa",
            phone_number="999999999",
            authority=None,
            role=None,
            user_id=None,
        )
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

        self.basic_headers = {
            "Authorization": f"Bearer {generate_jwt(self.valid_basic_jwt_payload)}"
        }
        self.admin_headers = {
            "Authorization": f"Bearer {generate_jwt(self.valid_jwt_payload)}"
        }

        self.mock_validate_email = Mock()
        self.mock_validate_email.return_value = True
        users_service.validate_email = self.mock_validate_email

    @patch("api.users.users_repository.UsersRepository.save")
    @patch("api.users.users_repository.UsersRepository.get_user_by_email")
    @patch("api.users.users_repository.UsersRepository.get_user_by_username")
    def test_create_valid_basic_user(
        self, mock_get_user_by_username, mock_get_user_by_email, mock_save
    ):
        mock_get_user_by_username.return_value = DatabaseResult(None)
        mock_get_user_by_email.return_value = DatabaseResult(None)
        mock_save.return_value = DatabaseResult(self.valid_new_user)

        response = OfflineHandler(create_user_handler).handle(
            ApiGatewayEvent(body=self.valid_new_user.as_camel_dict()).as_dict()
        )

        mock_get_user_by_username.assert_called_once()
        mock_get_user_by_email.assert_called_once()
        mock_save.assert_called_once()
        self.assertEqual(self.valid_new_user.as_json_response(), response["body"])
        self.assertEqual(200, response["statusCode"])

    def test_create_missing_field_basic_user(self):
        response = OfflineHandler(create_user_handler).handle(
            ApiGatewayEvent(body={}).as_dict()
        )
        self.assertEqual({"message": "A field is missing."}, response["body"])
        self.assertEqual(400, response["statusCode"])

    @patch("api.users.users_repository.UsersRepository.save")
    @patch("api.users.users_repository.UsersRepository.get_user_by_email")
    @patch("api.users.users_repository.UsersRepository.get_user_by_username")
    def test_create_valid_basic_user_username_and_email_taken(
        self, mock_get_user_by_username, mock_get_user_by_email, mock_save
    ):
        temp_user = self.valid_new_user
        temp_user.id = "adsf"
        mock_get_user_by_username.return_value = DatabaseResult(self.valid_new_user)
        mock_get_user_by_email.return_value = DatabaseResult(self.valid_new_user)

        response = OfflineHandler(create_user_handler).handle(
            ApiGatewayEvent(body=self.valid_new_user.as_camel_dict()).as_dict()
        )

        mock_get_user_by_username.assert_called_once()
        mock_get_user_by_email.assert_called_once()
        mock_save.assert_not_called()
        self.assertEqual(
            {"email": "Email is taken.", "username": "Username is taken."},
            response["body"],
        )
        self.assertEqual(400, response["statusCode"])

    @patch("api.users.users_repository.UsersRepository.save")
    @patch("api.users.users_repository.UsersRepository.get_user_by_email")
    @patch("api.users.users_repository.UsersRepository.get_user_by_username")
    def test_create_invalid_basic_user(
        self, mock_get_user_by_username, mock_get_user_by_email, mock_save
    ):
        mock_get_user_by_username.return_value = DatabaseResult(None)
        mock_get_user_by_email.return_value = DatabaseResult(None)
        mock_save.return_value = DatabaseResult(self.valid_new_user)

        response = OfflineHandler(create_user_handler).handle(
            ApiGatewayEvent(body=self.invalid_new_user.as_camel_dict()).as_dict()
        )

        self.assertEqual(
            {
                "email": "Invalid email.",
                "password": "Invalid password.",
                "username": "Invalid username.",
                "phoneNumber": "Invalid phone number.",
            },
            response["body"],
        )
        self.assertEqual(400, response["statusCode"])

    @patch("api.users.users_repository.UsersRepository.save")
    @patch("api.users.users_repository.UsersRepository.get_user_by_email")
    @patch("api.users.users_repository.UsersRepository.get_user_by_username")
    def test_create_valid_admin_user(
        self, mock_get_user_by_username, mock_get_user_by_email, mock_save
    ):
        mock_get_user_by_username.return_value = DatabaseResult(None)
        mock_get_user_by_email.return_value = DatabaseResult(None)
        mock_save.return_value = DatabaseResult(self.valid_new_user)

        response = OfflineHandler(create_admin_user_handler).handle(
            ApiGatewayEvent(
                body=self.valid_new_user.as_camel_dict(), headers=self.admin_headers
            ).as_dict()
        )

        mock_get_user_by_username.assert_called_once()
        mock_get_user_by_email.assert_called_once()
        mock_save.assert_called_once()
        self.assertEqual(self.valid_new_user.as_json_response(), response["body"])
        self.assertEqual(200, response["statusCode"])

    def test_create_missing_field_admin_user(self):
        response = OfflineHandler(create_admin_user_handler).handle(
            ApiGatewayEvent(body={}, headers=self.admin_headers).as_dict()
        )
        self.assertEqual({"message": "A field is missing."}, response["body"])
        self.assertEqual(400, response["statusCode"])

    @patch("api.users.users_repository.UsersRepository.save")
    @patch("api.users.users_repository.UsersRepository.get_user_by_email")
    @patch("api.users.users_repository.UsersRepository.get_user_by_username")
    def test_create_valid_admin_user_username_and_email_taken(
        self, mock_get_user_by_username, mock_get_user_by_email, mock_save
    ):
        temp_user = self.valid_new_user
        temp_user.id = "adsf"
        mock_get_user_by_username.return_value = DatabaseResult(self.valid_new_user)
        mock_get_user_by_email.return_value = DatabaseResult(self.valid_new_user)

        response = OfflineHandler(create_admin_user_handler).handle(
            ApiGatewayEvent(
                body=self.valid_new_user.as_camel_dict(), headers=self.admin_headers
            ).as_dict()
        )

        mock_get_user_by_username.assert_called_once()
        mock_get_user_by_email.assert_called_once()
        mock_save.assert_not_called()
        self.assertEqual(
            {"email": "Email is taken.", "username": "Username is taken."},
            response["body"],
        )
        self.assertEqual(400, response["statusCode"])

    @patch("api.users.users_repository.UsersRepository.save")
    @patch("api.users.users_repository.UsersRepository.get_user_by_email")
    @patch("api.users.users_repository.UsersRepository.get_user_by_username")
    def test_create_invalid_admin_user(
        self, mock_get_user_by_username, mock_get_user_by_email, mock_save
    ):
        mock_get_user_by_username.return_value = DatabaseResult(None)
        mock_get_user_by_email.return_value = DatabaseResult(None)
        mock_save.return_value = DatabaseResult(self.valid_new_user)

        response = OfflineHandler(create_admin_user_handler).handle(
            ApiGatewayEvent(
                body=self.invalid_new_user.as_camel_dict(), headers=self.admin_headers
            ).as_dict()
        )

        self.assertEqual(
            {
                "email": "Invalid email.",
                "password": "Invalid password.",
                "username": "Invalid username.",
                "phoneNumber": "Invalid phone number.",
            },
            response["body"],
        )
        self.assertEqual(400, response["statusCode"])

    def test_create_admin_user_unauthorized(self):
        response = OfflineHandler(create_admin_user_handler).handle(
            ApiGatewayEvent(body={}, headers=self.basic_headers).as_dict()
        )
        self.assertEqual({}, response["body"])
        self.assertEqual(401, response["statusCode"])

    def test_update_user_handler_valid_user(self):
        self.assertTrue(True)
