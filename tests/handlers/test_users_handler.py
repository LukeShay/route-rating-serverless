from unittest.mock import patch, Mock

from api.users.user import User
from api.handlers.users_handler import create_user_handler
from api.users import users_service
from tests.test_base import TestBase

from tests.utilities import ApiGatewayEvent, DatabaseResult


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

        response = create_user_handler(
            ApiGatewayEvent(body=self.valid_new_user.as_camel_dict()).as_dict(), None
        )

        self.assertEqual(self.valid_new_user.as_json_response(), response["body"])
        self.assertEqual(200, response["statusCode"])

    def test_create_missing_field_basic_user(self):
        response = create_user_handler(ApiGatewayEvent(body={}).as_dict(), None)
        self.assertEqual({"message": "A field is missing."}, response["body"])
        self.assertEqual(400, response["statusCode"])

    @patch("api.users.users_repository.UsersRepository.get_user_by_email")
    @patch("api.users.users_repository.UsersRepository.get_user_by_username")
    def test_create_valid_basic_user_username_and_email_taken(
        self, mock_get_user_by_username, mock_get_user_by_email
    ):
        temp_user = self.valid_new_user
        temp_user.id = "adsf"
        mock_get_user_by_username.return_value = DatabaseResult(self.valid_new_user)
        mock_get_user_by_email.return_value = DatabaseResult(self.valid_new_user)

        response = create_user_handler(
            ApiGatewayEvent(body=self.valid_new_user.as_camel_dict()).as_dict(), None
        )

        self.assertEqual(
            {"email": "Email is taken.", "username": "Username is taken."},
            response["body"],
        )
        self.assertEqual(400, response["statusCode"])
