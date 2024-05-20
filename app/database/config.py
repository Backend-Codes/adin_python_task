from pydantic import BaseSettings
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent / '.env'

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str

    class Config:
        env_file = env_path

settings = Settings()