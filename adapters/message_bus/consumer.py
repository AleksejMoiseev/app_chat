from classic.messaging_kombu import KombuConsumer
from kombu import Connection

from adapters.message_bus import broker_scheme
from adapters.message_bus.settings import ExchangeTopic


def send_message_to_manager(message):
    print(message)


def create_consumer(connection: Connection) -> KombuConsumer:

    consumer = KombuConsumer(connection=connection,
                             scheme=broker_scheme)

    consumer.register_function(
        send_message_to_manager, ExchangeTopic.queue.value,
    )

    return consumer
