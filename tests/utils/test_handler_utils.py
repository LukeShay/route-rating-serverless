from api.utils.handler_utils import setup_logger
import logging
from unittest import TestCase
import os


class TestHandlerUtils(TestCase):
    def setUp(self) -> None:
        root = logging.getLogger()

        for handler in root.handlers:
            root.removeHandler(handler)

        os.environ["LOG"] = "FALSE"

    def test_setup_logger_false(self):
        setup_logger()
        root = logging.getLogger()
        self.assertEqual(0, len(root.handlers))

    def test_setup_logger_true(self):
        os.environ["LOG"] = "TRUE"

        setup_logger()
        root = logging.getLogger()
        self.assertEqual(0, len(root.handlers))

    def test_no_setup_logger(self):
        root = logging.getLogger()
        self.assertEqual(0, len(root.handlers))
