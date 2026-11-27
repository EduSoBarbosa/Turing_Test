from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    gemini_api_key: SecretStr = SecretStr("")
    gemini_model: str = ""
    gemini_temperature: float = Field(0.7, ge=0, le=2)
    gemini_top_p: float = Field(0.95, gt=0, le=1)
    gemini_max_output_tokens: int = Field(256, gt=0)
    gemini_timeout_seconds: float = Field(30, ge=0.001)
    gemini_requests_per_minute: int = Field(20, gt=0)
    max_message_length: int = Field(2000, gt=0)
    max_messages_per_experiment: int = Field(10, gt=0)
    database_url: str = "sqlite:///./turing_test.db"
    admin_api_key: SecretStr = SecretStr("")
    cors_origins: str = "http://localhost:5173"

    @property
    def gemini_enabled(self) -> bool:
        return bool(self.gemini_api_key.get_secret_value().strip() and self.gemini_model.strip())
