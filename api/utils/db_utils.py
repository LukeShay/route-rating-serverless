import boto3
import logging
import os

PORT = 5432
DATABASE = "routerating"


def create_database_session():
    logging.debug("Creating database session.")
    return boto3.resource("dynamodb")


def get_users_table():
    return create_database_session().Table(os.getenv("DYNAMODB_USERS_TABLE"))


def get_ratings_table():
    return create_database_session().Table(os.getenv("DYNAMODB_RATINGS_TABLE"))


def get_gyms_table():
    return create_database_session().Table(os.getenv("DYNAMODB_GYMS_TABLE"))
