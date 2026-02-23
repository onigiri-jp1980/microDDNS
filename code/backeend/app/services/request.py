from fastapi import Request

class RequestService:
    def __init__(self, request: Request):
        self.request = request
        self.aws_event = request.scope.get('aws.event')
        self.aws_context = request.scope.get('aws.context')

    def get_aws_event(self) -> dict:
        return self.request.scope.get('aws.event')

    def get_aws_context(self) -> dict:
        return self.request.scope.get('aws.context')