class ScoreserviceApiError(Exception):
    def __init__(self, message: str = "Service is unavailable", name: str = "Scoreservice"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)

class ServiceError(ScoreserviceApiError):
    pass

class EntityDoesNotExistError(ScoreserviceApiError):
    pass

class EntityAlreadyExistsError(ScoreserviceApiError):
    pass

class InvalidOperationError(ScoreserviceApiError):
    pass

class AuthenticationFailed(ScoreserviceApiError):
    pass

class InvalidTokenError(ScoreserviceApiError):
    pass
