
"""Central configuration for the RoomReady application."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "sqlite:///./roomready.db"
    seed_dir: str = "seed"
    host: str = "0.0.0.0"
    port: int = 8080
