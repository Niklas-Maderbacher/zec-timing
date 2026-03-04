class TeamserviceApiError(Exception):
    def __init__(self, message: str = "Service is unavailable", name: str = "Teamservice"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)

class ServiceError(TeamserviceApiError):
    pass

class EntityDoesNotExistError(TeamserviceApiError):
    pass

class EntityAlreadyExistsError(TeamserviceApiError):
    pass

class InvalidOperationError(TeamserviceApiError):
    pass

class AuthenticationFailed(TeamserviceApiError):
    pass

class InvalidTokenError(TeamserviceApiError):
    pass

class InsufficientPermissions(TeamserviceApiError):
    pass
