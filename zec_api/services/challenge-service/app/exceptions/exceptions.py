class ChallengeserviceApiError(Exception):
    def __init__(self, message: str = "Service is unavailable", name: str = "Challengeservice"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)

class ServiceError(ChallengeserviceApiError):
    pass

class EntityDoesNotExistError(ChallengeserviceApiError):
    pass

class EntityAlreadyExistsError(ChallengeserviceApiError):
    pass

class InvalidOperationError(ChallengeserviceApiError):
    pass

class AuthenticationFailed(ChallengeserviceApiError):
    pass

class InvalidTokenError(ChallengeserviceApiError):
    pass
