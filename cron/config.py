

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    host: str = "localhost"
    port: int = 5434
    login: str = "postgres"
    password: str = "postgres"
    base_db: str = "postgres"
    driver: str = "postgresql+asyncpg"

    @property
    def url(self):
        return f"{self.driver}://{self.login}:{self.password}@{self.host}:{self.port}/{self.base_db}"
    
    interval_work: int = 30
    
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=os.getenv("ENV_PATH", ".env")
    )

settings = Config()