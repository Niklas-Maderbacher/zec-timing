class AuthserviceApiError(Exception):
    """base exception class"""

    def __init__(self, message: str = "", name: str = "Authservice"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)

class TokenHeaderRequired(AuthserviceApiError):
    pass

class InvalidTokenFormat(AuthserviceApiError):
    pass

class InvalidTokenHeader(AuthserviceApiError):
    pass

class PublicKeyNotFound(AuthserviceApiError):
    pass

class InvalidPublicKey(AuthserviceApiError):
    pass

class TokenExpired(AuthserviceApiError):
    pass

class InvalidClaims(AuthserviceApiError):
    pass

class InsufficientPermissions(AuthserviceApiError):
    pass

class KeycloakUnavailable(AuthserviceApiError):
    pass

class InvalidCredentials(AuthserviceApiError):
    pass

class TokenRefreshFailed(AuthserviceApiError):
    pass

class MissingRoles(AuthserviceApiError):
    pass

