import os
from pathlib import Path

from pydantic import BaseSettings
from dotenv import dotenv_values
from enum import Enum


BASE_DIR = Path(__file__).resolve().parent
CONF_DIR = os.path.join(BASE_DIR, '.env')

config = dotenv_values(CONF_DIR)

BROKER_URL = f"amqp://{config.get('USER')}:{config.get('PASSWORD')}@{config.get('HOST')}:{config.get('PORT')}//"


class ExchangeTopic(Enum):
    exchange = 'amq.fanout'
    exchange_type = 'fanout'
    queue = 'fan-1'


class RabbitConfigKombu(Enum):

    exchange = 'amq.direct'
    exchange_type = 'direct'
    routing_key = 'test'
    queue = 'My_Queu'


class Settings(BaseSettings):
    BROKER_URL: str


settings = Settings(BROKER_URL=BROKER_URL)


if __name__ == '__main__':
    print(settings.BROKER_URL=='amqp://user:password@localhost:5672//')