import warnings
from typing import Literal
from pydantic import computed_field, model_validator
from pydantic_core import MultiHostUrl
from typing_extensions import Self
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str
    API_STR: str = "/api"

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    KEYCLOAK_URL: str = ""
    KEYCLOAK_REALM: str = ""
    KEYCLOAK_ADMIN_CLIENT_ID: str = ""
    KEYCLOAK_ADMIN_CLIENT_SECRET: str = ""
    KEYCLOAK_CLIENT_ID: str = ""
    KEYCLOAK_CLIENT_SECRET: str = ""
    KEYCLOAK_TOKEN_URL: str = ""
    KEYCLOAK_JWKS_URL: str = ""
    KEYCLOAK_USER_URL: str = ""

    @computed_field
    @property
    def KEYCLOAK_REALM_URL(self) -> str:
        return f"{self.KEYCLOAK_URL}/realms/{self.KEYCLOAK_REALM}"
    
    @computed_field
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme="postgresql+psycopg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value in (None, "", "changethis"):
            message = f'The value of {var_name} is "{value}"; change it before deployment.'
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        return self

settings = Settings()
