from api.api_gateway import ApiGatewayEvent
from api.users.user import User
from api.users.users_service import UsersService
from api.utils.handler_utils import handler


@handler(database=True)
def new_user_handler(event: ApiGatewayEvent):
    users_service = UsersService(event.database_session)

    response = {}

    new_user = User.from_camel_dict(event.body)

    if not new_user.new_user_fields_present():
        return event.bad_request_response({"message": "A field is missing."})

    if users_service.get_user_by_email(new_user):
        response["email"] = "Email is taken."

    if users_service.get_user_by_username(new_user):
        response["username"] = "Username is taken."

    if len(response.keys()) != 0:
        return event.bad_request_response(response)

    user = users_service.create_basic_user(new_user)

    return event.ok_response(user.as_json_response())
