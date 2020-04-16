import os
from unittest import TestCase


class TestBase(TestCase):
    os.environ["TEST_RUN"] = "TRUE"
