import boto3
import logging


PORT = 5432
DATABASE = "routerating"


def create_database_session():
    logging.debug("Creating database session.")
    return boto3.resource("dynamodb")
