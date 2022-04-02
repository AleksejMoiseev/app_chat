import logging

from kombu import Connection
from adapters import message_bus

logging.basicConfig(level=logging.INFO)


class MessageBus:
    settings = message_bus.settings
    connection = Connection(settings.BROKER_URL)
    message_bus.broker_scheme.declare(connection)

    consumer = message_bus.create_consumer(
        connection
    )


MessageBus.consumer.run()
