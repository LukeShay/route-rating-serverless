import logging
import os
import traceback

from api.auth import Auth
from api.utils.db_utils import create_database_session
from api.api_gateway import ApiGatewayEvent, ApiGatewayResponse


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
    try:
        auth = Auth(args[0][0])

        if not auth.validate_jwt():
            return ApiGatewayResponse.forbidden_json_response()

        if admin_auth and not auth.is_admin():
            return ApiGatewayResponse.unauthorized_json_response()

        return function(
            ApiGatewayEvent(
                event,
                context,
                database_session,
                auth.get_jwt_payload().id,
                auth.get_jwt_payload().authorities,
            )
        )
    except Exception as e:
        logging.error("Exception raised while authenticating.")
        logging.error(traceback.format_exc())
        logging.exception(e)

        return ApiGatewayResponse.forbidden_json_response()


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
    if os.getenv("LOG", None) == "TRUE":
        logging.getLogger().setLevel(logging.DEBUG)
