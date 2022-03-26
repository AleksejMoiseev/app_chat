from pydantic import BaseSettings
from dotenv import dotenv_values


config = dotenv_values(".env")
DB_URL = f"mysql://{config.get('DB_USER')}:{config.get('DB_PASSWORD')}@{config.get('DB_HOST')}" \
         f":{config.get('DB_PORT')}/{config.get('DB_DATABASE')}"


class DBSettings(BaseSettings):
    DB_URL: str = DB_URL


if __name__ == '__main__':
    print(DB_URL)
