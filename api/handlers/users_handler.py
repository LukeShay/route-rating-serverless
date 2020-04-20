from api.api_gateway import ApiGatewayEvent
from api.users.user import User
from api.users.users_service import UsersService
from api.utils.handler_utils import handler, admin_handler, basic_handler


def create_user_helper(event: ApiGatewayEvent, new_user: User) -> dict:
    if not new_user.new_user_fields_present():
        return {"message": "A field is missing."}

    users_service = UsersService(event.database_session)
    new_user.email = new_user.email.lower()
    response = {}

    if users_service.get_user_by_email(new_user):
        response["email"] = "Email is taken."

    if users_service.get_user_by_username(new_user):
        response["username"] = "Username is taken."

    if len(response.keys()) > 0:
        return response

    if not users_service.valid_email(new_user):
        response["email"] = "Invalid email."

    if not users_service.valid_password(new_user):
        response["password"] = "Invalid password."

    if not users_service.valid_username(new_user):
        response["username"] = "Invalid username."

    if not users_service.valid_phone_number(new_user):
        response["phoneNumber"] = "Invalid phone number."

    return response


@handler(database=True)
def create_user_handler(event: ApiGatewayEvent):
    new_user = User.from_camel_dict(event.body)
    new_user.authority = "BASIC"
    new_user.role = "BASIC_ROLE"

    response = create_user_helper(event, new_user)

    if len(response.keys()):
        return event.bad_request_response(response)

    return event.ok_response(
        UsersService(event.database_session).create_user(new_user).as_json_response()
    )


@admin_handler(database=True)
def create_admin_user_handler(event: ApiGatewayEvent):
    new_user = User.from_camel_dict(event.body)
    new_user.authority = "ADMIN"
    new_user.role = "ADMIN_ROLE"

    response = create_user_helper(event, new_user)

    if len(response.keys()):
        return event.bad_request_response(response)

    return event.ok_response(
        UsersService(event.database_session).create_user(new_user).as_json_response()
    )


@basic_handler(database=True)
def update_user_handler(event: ApiGatewayEvent):
    body = User.from_camel_dict(event.body)
    return event.ok_response(body)
