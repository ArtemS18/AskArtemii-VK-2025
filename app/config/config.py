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

class EndpointConfig(BaseModel):
    base: str = "/"
    question: str = "/questions"
    user: str = "/users"
    ask: str = "/asks"
    hot_tags: str = "/hot"
    login: str = "/login"
    singup: str = "/signup"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP__",
        env_nested_delimiter="__",
        str_to_upper=True
    )
    base_dir: str = "app/"
    server: ServerConfig
    template: TemplateConfig
    endpoint: EndpointConfig

    @property
    def template_path(self):
        return self.base_dir+self.template.dir
    
config = Config(_env_file=os.getenv("APP__ENV_PATH", ".env"))




# BASE_APP_DIR = "app/"

# TEMPLATE_PATH = BASE_APP_DIR + "templates"

# HOST = os.getenv("APP__LOCALHOST","localhost")
# PORT = os.getenv("APP__PORT",8080)
# MAX_WORKERS = os.getenv("APP__MAX_WORKERS",1)
# RELOAD = os.getenv("APP__RELOAD",True)
