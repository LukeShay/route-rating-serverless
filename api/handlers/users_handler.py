import logging

from api.api_gateway import ApiGatewayEvent
from api.users.user import User
from api.users.users_service import UsersService
from api.utils.handler_utils import handler, admin_handler, basic_handler


log = logging.getLogger(__file__)


def validate_user_fields(users_service: UsersService, user: User) -> dict:
    response = {}

    if not users_service.valid_email(user):
        response["email"] = "Invalid email."

    if not users_service.valid_password(user):
        response["password"] = "Invalid password."

    if not users_service.valid_username(user):
        response["username"] = "Invalid username."

    if not users_service.valid_phone_number(user):
        response["phoneNumber"] = "Invalid phone number."

    return response


def create_user_helper(event: ApiGatewayEvent, new_user: User) -> dict:
    users_service = UsersService(event.database_session)

    response = {}

    if not new_user.new_user_fields_present():
        return {"message": "A field is missing."}

    new_user.email = new_user.email.lower()

    if users_service.get_user_by_email(new_user):
        response["email"] = "Email is taken."

    if users_service.get_user_by_username(new_user):
        response["username"] = "Username is taken."

    return (
        response
        if len(response.keys()) > 0
        else validate_user_fields(users_service, new_user)
    )


@handler(database=True)
def create_user_handler(event: ApiGatewayEvent) -> dict:
    new_user = User.from_camel_dict(event.body)
    new_user.authority = "BASIC"
    new_user.role = "BASIC_ROLE"

    response = create_user_helper(event, new_user)

    if len(response.keys()) > 0:
        return event.bad_request_response(response)

    new_user.email = new_user.email.lower()

    return event.ok_response(
        UsersService(event.database_session).create_user(new_user).as_json_response()
    )


@admin_handler(database=True)
def create_admin_user_handler(event: ApiGatewayEvent) -> dict:
    new_user = User.from_camel_dict(event.body)
    new_user.authority = "ADMIN"
    new_user.role = "ADMIN_ROLE"

    response = create_user_helper(event, new_user)

    if len(response.keys()) > 0:
        return event.bad_request_response(response)

    new_user.email = new_user.email.lower()

    return event.ok_response(
        UsersService(event.database_session).create_user(new_user).as_json_response()
    )


@basic_handler(database=True)
def update_user_handler(event: ApiGatewayEvent) -> dict:
    updated_user = User.from_camel_dict(event.body)

    if event.user_id != updated_user.id:
        return event.unauthorized_response()

    users_service = UsersService(event.database_session)

    current_user = users_service.get_user_by_id(updated_user)
    updated_user += current_user
    response = {}

    updated_user.email = updated_user.email.lower()

    if updated_user.email != current_user.email and users_service.get_user_by_email(
        updated_user
    ):
        response["email"] = "Email is taken."

    if (
        updated_user.username != current_user.username
        and users_service.get_user_by_username(updated_user)
    ):
        response["username"] = "Username is taken."

    if len(response.keys()) > 0:
        return event.bad_request_response(response)

    response = validate_user_fields(users_service, updated_user)

    if len(response.keys()) > 0:
        return event.bad_request_response(response)

    if current_user.password != updated_user.password:
        updated_user.password = users_service.encrypt_password(updated_user.password)

    return event.ok_response(users_service.update_user(updated_user).as_json_response())
