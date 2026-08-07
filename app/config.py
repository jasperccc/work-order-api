from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Work Order API"
    environment: Literal["development", "test", "production"] = "development"

    model_config = SettingsConfigDict(
        env_prefix="WORK_ORDER_",
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
