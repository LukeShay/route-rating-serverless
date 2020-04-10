import logging
import sys
import os


def setup_logger():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    root.addHandler(handler)


def log(function):
    def wrapper(*args, **kwargs):
        if os.getenv("LOG", None) == "TRUE":
            setup_logger()
        return function(*args)

    return wrapper
