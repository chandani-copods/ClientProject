from typing import Annotated, Any, Literal
from uuid import UUID
from pydantic import AnyUrl, BeforeValidator, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        env_override_existing_values=True,
    )
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440  # 1 day

    ENVIRONMENT: Literal["development", "staging", "production"] = "production"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    DEFAULT_ROLE_ID: int = 3
    # Permissions
    PERMISSION_PLATFORM_ADMIN: str = "all_permission"
   
    PERMISSION_ALL_CLIENT: str = "all_client_permission"
    PERMISSION_SINGLE_CLIENT: str = "single_client_permission"
    SCOPE_ALL_CLIENT_ACCESS: str = "default_scope_all_client_access"

    # Postgres
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    POSTGRES_DB_OWNER: str = "postgres"

    CHAT_COMPLETIONS_API_URL: str = ""
    CHAT_DEFAULT_MODEL: str = "gpt-3.5-turbo"
    CHAT_TEMPERATURE: float = 0.7
    CHAT_MAX_TOKENS: int = 512


    # Internal API
    # REPORTS_BASE_URL: str = "http://host.docker.internal:5001"

    # OTP
    OTP_EXPIRE_MINUTES: int = 3
    OTP_ATTEMPTS: int = 3

    # DEFAULT IDs
    # DEFAULT_PG_CLUSTER_ID: UUID = "600e8b20-588c-49e6-b0c4-dcdae573fc22"

    # Database
    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS]


settings = Settings()
