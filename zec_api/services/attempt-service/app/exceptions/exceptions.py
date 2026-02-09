class AttemptserviceApiError(Exception):
    def __init__(self, message: str = "Service is unavailable", name: str = "Attemptservice"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)

class ServiceError(AttemptserviceApiError):
    pass

class EntityDoesNotExistError(AttemptserviceApiError):
    pass

class EntityAlreadyExistsError(AttemptserviceApiError):
    pass

class InvalidOperationError(AttemptserviceApiError):
    pass

class AuthenticationFailed(AttemptserviceApiError):
    pass

class InvalidTokenError(AttemptserviceApiError):
    pass
