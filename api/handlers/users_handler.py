from api.api_gateway import ApiGatewayEvent
from api.users.user import User
from api.users.users_service import UsersService
from api.utils.handler_utils import handler, admin_handler


def create_user_helper(event: ApiGatewayEvent, new_user: User):
    users_service = UsersService(event.database_session)

    response = {}

    if not new_user.new_user_fields_present():
        return event.bad_request_response({"message": "A field is missing."})

    new_user.email = new_user.email.lower()

    if users_service.get_user_by_email(new_user):
        response["email"] = "Email is taken."

    if users_service.get_user_by_username(new_user):
        response["username"] = "Username is taken."

    if len(response.keys()) > 0:
        return event.bad_request_response(response)

    if not users_service.valid_email(new_user):
        response["email"] = "Invalid email."

    if not users_service.valid_password(new_user):
        response["password"] = "Invalid password."

    if not users_service.valid_username(new_user):
        response["username"] = "Invalid username."

    if not users_service.valid_phone_number(new_user):
        response["phoneNumber"] = "Invalid phone number."

    if len(response.keys()) > 0:
        return event.bad_request_response(response)

    new_user.authority = "BASIC"
    new_user.role = "BASIC_ROLE"
    user = users_service.create_user(new_user)

    return event.ok_response(user.as_json_response())


@handler(database=True)
def create_user_handler(event: ApiGatewayEvent):
    new_user = User.from_camel_dict(event.body)
    new_user.authority = "BASIC"
    new_user.role = "BASIC_ROLE"
    return create_user_helper(event, new_user)


@admin_handler(database=True)
def create_admin_user_handler(event: ApiGatewayEvent):
    new_user = User.from_camel_dict(event.body)
    new_user.authority = "ADMIN"
    new_user.role = "ADMIN_ROLE"
    return create_user_helper(event, new_user)