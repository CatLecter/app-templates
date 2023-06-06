from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')


@dataclass
class Settings:
    pg_user: str = getenv('POSTGRES_USER', 'user')
    pg_password: str = getenv('POSTGRES_PASSWORD', 'password')
    pg_host: str = getenv('POSTGRES_HOST', '127.0.0.1')
    pg_port: int = getenv('POSTGRES_PORT', 5432)
    pg_db: str = getenv('POSTGRES_DB', 'db')
    app_host: str = getenv('APP_HOST', '127.0.0.1')
    app_port: int = getenv('APP_PORT', 8000)
    reload: bool = getenv('RELOAD', True)
    log_level: str = getenv('LOG_LEVEL', 'debug')


settings = Settings()
