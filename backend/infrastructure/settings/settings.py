from pydantic_settings import BaseSettings, SettingsConfigDict

from infrastructure.settings.object_storage import ObjectStorage
from infrastructure.settings.postgres import Postgres
from infrastructure.settings.sq import SQ
from infrastructure.settings.sso import SSO


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    postgres: Postgres
    object_storage: ObjectStorage
    sso: SSO
    sq: SQ

    def get_postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres.username}:{self.postgres.password}@"
            f"{self.postgres.host}:{self.postgres.port}/{self.postgres.db_name}"
        )


settings = Settings()  # type: ignore
