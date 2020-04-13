from queries import Session


class ApiGatewayEvent:
    def __init__(
        self,
        event,
        context,
        database_session=None,
        user_id=None,
        user_authority=None,
        headers=None,
    ):
        self._event = event
        self._context = context
        self._database_session = database_session
        self._user_id = user_id
        self._user_authority = user_authority
        self._headers = headers if headers else {}

    @property
    def body(self) -> dict:
        """
        :return: The body from the API Gateway event as a dict
        """
        return self._event.get("body", {})

    @property
    def database_session(self) -> Session:
        """
        :return: The queries database session
        """
        return self._database_session

    @property
    def user_id(self) -> str or None:
        """
        :return: The currently signed in user id or none
        """
        return self._user_id

    @property
    def user_authority(self) -> str or None:
        """
        :return: The currently signed in user authority or none
        """
        return self._user_authority

    def ok_json_response(self, body=None, headers=None):
        if not headers:
            headers = {}
        return ApiGatewayResponse.ok_json_response(body, {**self._headers, **headers})

    def unauthorized_json_response(self, body=None, headers=None):
        if not headers:
            headers = {}
        return ApiGatewayResponse.unauthorized_json_response(
            body, {**self._headers, **headers}
        )

    def forbidden_json_response(self, body=None, headers=None):
        if not headers:
            headers = {}
        return ApiGatewayResponse.forbidden_json_response(
            body, {**self._headers, **headers}
        )


class ApiGatewayResponse:
    def __init__(self, status_code=200, body=None, headers=None):
        if not headers:
            headers = {}

        self.status_code = status_code
        self.body = body
        self.headers = headers

    @classmethod
    def ok_json_response(cls, body=None, headers=None):
        if not headers:
            headers = {}

        headers.update({"Content-type": "application/json"})

        return cls(body=body, headers=headers).as_dict()

    @classmethod
    def unauthorized_json_response(cls, body=None, headers=None):
        if not headers:
            headers = {}

        headers.update({"Content-type": "application/json"})

        return cls(status_code=401, body=body).as_dict()

    @classmethod
    def forbidden_json_response(cls, body=None, headers=None):
        if not headers:
            headers = {}

        headers.update({"Content-type": "application/json"})

        return cls(status_code=403, body=body).as_dict()

    def as_dict(self):
        return {
            "statusCode": self.status_code,
            "body": self.body,
            "headers": self.headers,
        }
