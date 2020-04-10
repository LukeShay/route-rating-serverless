from api.utils.response_utils import ApiGatewayResponse
from api.auth import basic_auth, admin_auth
from api.utils.logging_utils import log


@log
@basic_auth
def basic_auth_handler(event, context):
    return ApiGatewayResponse.ok_json_response(
        {"message": "successful basic authentication"}
    )


@log
@admin_auth
def admin_auth_handler(event, context):
    return ApiGatewayResponse.ok_json_response(
        {"message": "successful admin authentication"}
    )
