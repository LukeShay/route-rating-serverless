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
