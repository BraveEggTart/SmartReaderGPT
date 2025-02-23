import logging
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Infomation
    TITLE: str = "Smart Reader GPT"
    DESCRIPTION: str = "A file reader base on GPT"
    VERSION: str = "0.1.0"

    # CORS
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    # project path
    PROJECT_ROOT: Path = Path(__file__).resolve().parent
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # datetime format
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"
    DATETIME_TIMEZONE: str = "Asia/Shanghai"

    # openssl rand -hex 32
    SECRET_KEY: str = ""
    PREFIX: str = "/api"

    # OPENAI SECRET
    OPENAI_KEY: str = ""
    OPENAI_PROXY: str = ""

    DEBUGGER: bool = False
    LOG_LEVEL: int = logging.INFO

    class Config:
        env_file = ".env"


settings = Settings()
