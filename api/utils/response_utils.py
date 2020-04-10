class ApiGatewayResponse:
    def __init__(self, status_code=200, body=None):
        self.status_code = status_code
        self.body = body

    @classmethod
    def ok_json_response(cls, body=None):
        return cls(body=body).as_dict()

    @classmethod
    def unauthorized_json_response(cls, body=None):
        return cls(status_code=401, body=body).as_dict()

    @classmethod
    def forbidden_json_response(cls, body=None):
        return cls(status_code=403, body=body).as_dict()

    def as_dict(self):
        return {"statusCode": self.status_code, "body": self.body}
