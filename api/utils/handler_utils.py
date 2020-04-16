import logging
import os
import traceback
import sys

from api.auth import Auth
from api.utils.db_utils import create_database_session
from api.api_gateway import ApiGatewayEvent


def validate_kwargs(*args, **kwargs):
    logging.debug(args)
    if len(args[0][0]) != 2:
        raise InvalidRequestException

    return args[0][0]


def get_event_params(database, *args, **kwargs):
    event, context = validate_kwargs(args, kwargs)

    database_session = create_database_session() if database else None

    return event, context, database_session


def validate_jwt(
    function, event, context, database_session, admin_auth, *args, **kwargs
):
    api_event = ApiGatewayEvent(event, context, database_session, None, None, None)
    try:
        auth = Auth(args[0][0])

        valid, jwt_token, refresh_token = auth.validate_jwt()

        if not valid:
            return api_event.forbidden_response()

        if admin_auth and not auth.is_admin():
            return api_event.unauthorized_response()

        return function(
            ApiGatewayEvent(
                event,
                context,
                database_session,
                auth.get_jwt_payload().id,
                auth.get_jwt_payload().authorities,
                headers={"Authorization": jwt_token, "Refresh": refresh_token},
            )
        )
    except Exception as e:
        logging.error("Exception raised while authenticating.")
        logging.error(traceback.format_exc())
        logging.exception(e)

        return api_event.forbidden_response()


def handler(database):
    def decorator(function):
        def wrapper(*args, **kwargs):
            setup_logger()
            event, context, database_session = get_event_params(database, args, kwargs)
            return function(ApiGatewayEvent(event, context, database_session))

        return wrapper

    return decorator


def admin_handler(database):
    def decorator(function):
        def wrapper(*args, **kwargs):
            setup_logger()
            event, context, database_session = get_event_params(database, args, kwargs)
            return validate_jwt(
                function, event, context, database_session, True, args, kwargs
            )

        return wrapper

    return decorator


def basic_handler(database):
    def decorator(function):
        def wrapper(*args, **kwargs):
            setup_logger()
            event, context, database_session = get_event_params(database, args, kwargs)
            return validate_jwt(
                function, event, context, database_session, False, args, kwargs
            )

        return wrapper

    return decorator


class InvalidRequestException(Exception):
    def __init__(self):
        super().__init__()


def setup_logger():
    handlers = []
    basic_format = logging.Formatter(logging.BASIC_FORMAT)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.ERROR)

    if os.getenv("LOG", None) == "TRUE" or os.getenv("TEST_RUN") == "TRUE":
        stdout_handler.setLevel(logging.DEBUG)

    stdout_handler.setFormatter(basic_format)
    handlers.append(stdout_handler)

    # file_handler = logging.FileHandler("route-rating.log")
    # file_handler.setLevel(logging.DEBUG)
    # file_handler.setFormatter(basic_format)
    # handlers.append(file_handler)

    logging.basicConfig(level=logging.DEBUG, handlers=handlers, force=True)
