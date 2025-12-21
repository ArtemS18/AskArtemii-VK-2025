from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
import os

class ServerConfig(BaseModel):
    host: str = "localhost"
    port: int = 8080
    max_workers: int  = 1
    reload: bool = True

class TemplateConfig(BaseModel):
    dir: str = "templates"

class DBConfig(BaseModel):
    host: str = "localhost"
    port: int = 5434
    login: str = "postgres"
    password: str = "postgres"
    base_db: str = "postgres"
    driver: str = "postgresql+asyncpg"

    @property
    def url(self):
        return f"{self.driver}://{self.login}:{self.password}@{self.host}:{self.port}/{self.base_db}"
    
class MinioConfig(BaseModel):
    host: str = "localhost"
    port: int = 9000
    access_key: str = "minio"
    secret_key: str = "minio123"

    @property
    def url(self):
        return f"http://{self.host}:{self.port}"

class EndpointConfig(BaseModel):
    base: str = "/"
    question: str = "/questions"
    user: str = "/profile"
    ask: str = "/asks"
    tags: str = "/tags"
    hot: str="/hot"
    login: str = "/login"
    singup: str = "/signup"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=os.getenv("ENV_PATH", ".env")
    )
    base_dir: str = "app/"
    server: ServerConfig
    template: TemplateConfig
    endpoint: EndpointConfig
    db: DBConfig
    minio: MinioConfig
    local_storage: bool = True
    local_storage_dir: str = "media/avatars"
    local_storage_url: str = "http://localhost:8080"

    @property
    def template_path(self):
        return self.base_dir+self.template.dir
    
config = Config()


api_path = config.endpoint

BASE_IMG = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4JCuHyuURcCyeNEc9v4iOma3HVgZgDSMaIQ&s"
