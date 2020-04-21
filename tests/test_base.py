import os
from unittest import TestCase
from unittest.mock import Mock

from api.users import users_service
from api.users.users_service import UsersService


class TestBase(TestCase):
    os.environ["TEST_RUN"] = "TRUE"

    @classmethod
    def setUpClass(cls):
        cls.users_service = UsersService()
        cls.mock_validate_email = Mock(return_value=True)
        users_service.validate_email = cls.mock_validate_email
