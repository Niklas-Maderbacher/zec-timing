class UserserviceApiError(Exception):
    def __init__(self, message: str = "Service is unavailable", name: str = "Userservice"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)

class ServiceError(UserserviceApiError):
    pass

class EntityDoesNotExistError(UserserviceApiError):
    pass

class EntityAlreadyExistsError(UserserviceApiError):
    pass

class InvalidOperationError(UserserviceApiError):
    pass

class AuthenticationFailed(UserserviceApiError):
    pass

class InvalidTokenError(UserserviceApiError):
    pass
