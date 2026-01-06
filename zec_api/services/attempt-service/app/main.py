from fastapi import FastAPI, Request, status
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from app.api.main import api_router
from app.core.config import settings
from app.database.session import engine, Base
from typing import Callable
from app.exceptions.exceptions import (
    AuthenticationFailed,
    AttemptserviceApiError,
    EntityDoesNotExistError,
    InvalidOperationError,
    InvalidTokenError,
    ServiceError,
    EntityAlreadyExistsError,
)

def cstm_generate_unique_id(route: APIRoute) -> str:
    if route.tags and len(route.tags) > 0:
        return f"{route.tags[0]}-{route.name}"
    else:
        return f"untagged-{route.name}"

app = FastAPI(
    title="Attempt Service API",
    openapi_url=f"{settings.API_STR}/openapi.json",
    generate_unique_id_function=cstm_generate_unique_id,
)

app.include_router(api_router, prefix=settings.API_STR)
Base.metadata.create_all(bind=engine)

def create_exception_handler(
    status_code: int, initial_detail: str
) -> Callable[[Request, AttemptserviceApiError], JSONResponse]:
    detail = {"message": initial_detail}
    async def exception_handler(_: Request, exc: AttemptserviceApiError) -> JSONResponse:
        if exc.message:
            detail["message"] = exc.message
        if exc.name:
            detail["message"] = f"{detail['message']} [{exc.name}]"
        return JSONResponse(
            status_code=status_code, content={"detail": detail["message"]}
        )
    return exception_handler

app.add_exception_handler(
    exc_class_or_status_code=EntityDoesNotExistError,
    handler=create_exception_handler(
        status.HTTP_404_NOT_FOUND, "Entity does not exist."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidOperationError,
    handler=create_exception_handler(
        status.HTTP_400_BAD_REQUEST, "Can't perform the operation."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=AuthenticationFailed,
    handler=create_exception_handler(
        status.HTTP_401_UNAUTHORIZED,
        "Authentication failed.",
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidTokenError,
    handler=create_exception_handler(
        status.HTTP_401_UNAUTHORIZED, "Invalid token, please re-authenticate again."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=EntityAlreadyExistsError,
    handler=create_exception_handler(
        status.HTTP_409_CONFLICT, "Entity already exists."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=ServiceError,
    handler=create_exception_handler(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "A service seems to be down, try again later.",
    ),
)
