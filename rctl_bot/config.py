from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_token: str = Field(alias="BOT_TOKEN")
    admin_telegram_ids: frozenset[int] = Field(alias="ADMIN_TELEGRAM_IDS")

    @field_validator("admin_telegram_ids", mode="before")
    @classmethod
    def parse_admin_telegram_ids(cls, value: object) -> frozenset[int]:
        if isinstance(value, str):
            return frozenset(
                int(item.strip()) for item in value.split(",") if item.strip()
            )
        if isinstance(value, int):
            return frozenset({value})
        return frozenset(value)  # type: ignore[arg-type]
