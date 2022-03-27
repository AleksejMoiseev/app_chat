import os
from pathlib import Path

from pydantic import BaseSettings
from dotenv import dotenv_values
import enum


BASE_DIR = Path(__file__).resolve().parent
CONF_DIR = os.path.join(BASE_DIR, '.env')


class CONF(enum.Enum):
    default_limit = 5


config = dotenv_values(CONF_DIR)
DB_URL = f"mysql://{config.get('DB_USER')}:{config.get('DB_PASSWORD')}@{config.get('DB_HOST')}" \
         f":{config.get('DB_PORT')}/{config.get('DB_DATABASE')}"


class DBSettings(BaseSettings):
    DB_URL: str = DB_URL


settings = DBSettings()

if __name__ == '__main__':
    settings = DBSettings()
    print(settings.DB_URL)
