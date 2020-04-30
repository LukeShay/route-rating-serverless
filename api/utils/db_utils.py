from queries import uri, Session
from typing import Optional
import logging
import os


PORT = 5432
DATABASE = "routerating"


def create_database_session() -> Optional[Session]:
    logging.debug("Creating database session.")

    username = os.getenv("DATABASE_USERNAME")
    password = os.getenv("DATABASE_PASSWORD")
    url = os.getenv("DATABASE_URL")
    test_run = os.getenv("TEST_RUN")

    if test_run == "TRUE":
        return None

    if not username or not password or not url:
        logging.error(
            "One of the following environment variables is not set: DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_URL"
        )
        raise DatabaseConnectionException

    return Session(uri(url, PORT, DATABASE, username, password))


class DatabaseConnectionException(Exception):
    def __str__(self):
        return "There was an error with the database connection."
