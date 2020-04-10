from api.utils.logging_utils import log, setup_logger
import logging
from unittest import TestCase
import os


class TestLoggingUtils(TestCase):
    def setUp(self) -> None:
        root = logging.getLogger()

        for handler in root.handlers:
            root.removeHandler(handler)

        os.environ["LOG"] = "FALSE"

    def test_setup_logger(self):
        setup_logger()
        root = logging.getLogger()
        self.assertEqual(1, len(root.handlers))

    def test_no_setup_logger(self):
        root = logging.getLogger()

        for handler in root.handlers:
            root.removeHandler(handler)

        root = logging.getLogger()
        self.assertEqual(0, len(root.handlers))

    def test_log_decorator_false(self):
        os.environ["LOG"] = "FALSE"
        self.log_decorator()

        root = logging.getLogger()
        self.assertEqual(0, len(root.handlers))

    def test_log_decorator_true(self):
        os.environ["LOG"] = "TRUE"
        self.log_decorator()

        root = logging.getLogger()
        self.assertEqual(1, len(root.handlers))

    @log
    def log_decorator(self):
        return
