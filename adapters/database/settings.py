from pydantic import BaseSettings
from dotenv import dotenv_values


config = dotenv_values(".env")
DB_URL = f"mysql://{config.get('DB_USER')}:{config.get('DB_PASSWORD')}@{config.get('DB_HOST')}" \
         f":{config.get('DB_PORT')}/{config.get('DB_DATABASE')}"


class DBSettings(BaseSettings):
    DB_URL: str = 'mysql://exchange:exchange@localhost:3306/bootcamp'


settings = DBSettings()

if __name__ == '__main__':
    settings = DBSettings()
    print(settings.DB_URL)
