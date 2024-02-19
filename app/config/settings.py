from pathlib import Path
from typing import Any, List, Optional, Union

from dotenv import load_dotenv
from pydantic import PostgresDsn, field_validator, ValidationError
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings

from app.logs import logger

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


class Settings(BaseSettings):
    REDIS_PORT: int = 6379
    REDIS_HOST: str = None

    @field_validator("REDIS_PORT")
    def assemble_redis_port(cls, v: Union[str, List[str]], info: FieldValidationInfo) -> Any:

        if v:
            return v
        else:
            return 6378

    @field_validator("REDIS_HOST")
    def assemble_redis_host(cls, v: Union[str, List[str]]) -> Any:

        if v:
            return v
        else:
            return 'rq_redis'

    PROJECT_NAME: str
    CODEFORCE_API_URL: str = 'https://codeforces.com/'
    BOT_TOKEN: str

    """DATABASE CONFIG"""
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        user = info.data.get("POSTGRES_USER")
        password = info.data.get("POSTGRES_PASSWORD")
        host = info.data.get("POSTGRES_SERVER")
        db = info.data.get("POSTGRES_DB")

        if all([user, password, host, db]):
            return f"postgresql+asyncpg://{user}:{password}@{host}/{db}"
        else:
            return None

    # PYTHONPATH
    PYTHONPATH: str

    class Config:
        case_sensitive = True


try:
    settings = Settings()
except ValidationError as err:
    logger.error(f"Settings validation error, check your .env file or docker environments settings:\n{err.json()}")
