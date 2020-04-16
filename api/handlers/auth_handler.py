from api.api_gateway import ApiGatewayEvent
from api.users.users_service import UsersService
from api.utils.handler_utils import handler, admin_handler, basic_handler
from api.users.user import User
import logging


@basic_handler(database=False)
def basic_auth_handler(event: ApiGatewayEvent):
    return event.ok_response({"id": event.user_id, "authority": event.user_authority})


@admin_handler(database=False)
def admin_auth_handler(event: ApiGatewayEvent):
    return event.ok_response({"id": event.user_id, "authority": event.user_authority})


@handler(database=True)
def login_handler(event: ApiGatewayEvent):
    logging.info(event)

    users_service = UsersService(event.database_session)
    user, headers = users_service.login(User.from_camel_dict(event.body))

    if not user:
        return event.forbidden_response()

    return event.ok_response(user.as_json_response(), headers)
