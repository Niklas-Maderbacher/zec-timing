from fastapi import FastAPI, Request, status
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from app.database.session import engine, Base
from typing import Callable
from app.api.main import api_router
from app.core.config import settings
from app.exceptions.exceptions import (
    AuthserviceApiError,
    TokenHeaderRequired,
    InvalidTokenFormat,
    InvalidTokenHeader,
    PublicKeyNotFound,
    InvalidPublicKey,
    TokenExpired,
    InvalidClaims,
    InsufficientPermissions,
    MissingRoles,
    KeycloakUnavailable,
    TokenRefreshFailed,
    InvalidCredentials,
)

def cstm_generate_unique_id(route: APIRoute) -> str:
    if route.tags and len(route.tags) > 0:
        return f"{route.tags[0]}-{route.name}"
    else:
        return f"untagged-{route.name}"

app = FastAPI(
    title="Auth Service API",
    openapi_url=f"{settings.API_STR}/openapi.json",
    generate_unique_id_function=cstm_generate_unique_id,
)

app.include_router(api_router, prefix=settings.API_STR)
Base.metadata.create_all(bind=engine)

def create_exception_handler(
    status_code: int, initial_detail: str
) -> Callable[[Request, AuthserviceApiError], JSONResponse]:
    detail = {"message": initial_detail}
    async def exception_handler(_: Request, exc: AuthserviceApiError) -> JSONResponse:
        if exc.message:
            detail["message"] = exc.message
        if exc.name:
            detail["message"] = f"{detail['message']} [{exc.name}]"
        return JSONResponse(
            status_code=status_code, content={"detail": detail["message"]}
        )
    return exception_handler

app.add_exception_handler(
    exc_class_or_status_code=TokenHeaderRequired,
    handler=create_exception_handler(
        status.HTTP_401_UNAUTHORIZED, "No Token provided."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidTokenFormat,
    handler=create_exception_handler(
        status.HTTP_401_UNAUTHORIZED, "Malformed Token."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidTokenHeader,
    handler=create_exception_handler(
        status.HTTP_401_UNAUTHORIZED, "Invalid Header Format."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=TokenExpired,
    handler=create_exception_handler(
        status.HTTP_401_UNAUTHORIZED, "Token Expired."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidCredentials,
    handler=create_exception_handler(
        status.HTTP_401_UNAUTHORIZED, "Invalid credentials provided."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=TokenRefreshFailed,
    handler=create_exception_handler(
        status.HTTP_401_UNAUTHORIZED, "Token refresh failed."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=InsufficientPermissions,
    handler=create_exception_handler(
        status.HTTP_403_FORBIDDEN, "User lacks permissions."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=MissingRoles,
    handler=create_exception_handler(
        status.HTTP_403_FORBIDDEN, "No roles assigned to user."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=PublicKeyNotFound,
    handler=create_exception_handler(
        status.HTTP_500_INTERNAL_SERVER_ERROR, "Public key not found."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidPublicKey,
    handler=create_exception_handler(
        status.HTTP_500_INTERNAL_SERVER_ERROR, "Invalid public key."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidClaims,
    handler=create_exception_handler(
        status.HTTP_500_INTERNAL_SERVER_ERROR, "Invalid token claims."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=KeycloakUnavailable,
    handler=create_exception_handler(
        status.HTTP_503_SERVICE_UNAVAILABLE, "Keycloak service unavailable."
    ),
)