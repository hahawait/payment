from dataclasses import dataclass
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class AppConfig(BaseConfig):
    MODE: Literal["DEV", "TEST", "PROD", "LOCAL"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARN", "ERROR", "FATAL"]
    PROFILING_ENABLED: bool
    TITLE: str
    DESCRIPTION: str
    VERSION: str
    SENTRY_DSN: str | None = None
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    @property
    def is_production(self) -> bool:
        return self.MODE == "PROD"

    @property
    def is_dev(self) -> bool:
        return self.MODE == "DEV"

    @property
    def is_local(self) -> bool:
        return self.MODE == "LOCAL"


class PGConfig(BaseConfig):
    PG_HOST: str
    PG_NAME: str
    PG_PORT: int
    PG_PASS: str
    PG_USER: str

    @property
    def pg_database_url(self) -> str:
        user = f"{self.PG_USER}:{self.PG_PASS}"
        database = f"{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}"
        return f"postgresql+asyncpg://{user}@{database}"


class RPConfig(BaseConfig):
    RP_SERVER: str
    CONSUME_TOPIC: str
    CONSUME_GROUP: str
    SECURITY_PROTOCOL: str = "SASL_PLAINTEXT"
    SASL_MECHANISM: str = "SCRAM-SHA-512"
    RP_PASS: str
    RP_USER: str


class AuthConfig(BaseConfig):
    ALGORITHM: str
    PUBLIC_KEY: str


class TinkoffConfig(BaseConfig):
    TOKEN: str
    URL: str
    SEND_INVOICE: str


@dataclass
class Config:
    app: AppConfig
    pg: PGConfig
    rp: RPConfig
    auth: AuthConfig
    tinkoff: TinkoffConfig


def get_config() -> Config:
    return Config(
        app=AppConfig(),
        pg=PGConfig(),
        rp=RPConfig(),
        auth=AuthConfig(),
        tinkoff=TinkoffConfig()
    )
