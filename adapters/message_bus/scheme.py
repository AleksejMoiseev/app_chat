from classic.messaging_kombu import BrokerScheme
from kombu import Exchange, Queue
from adapters.message_bus.settings import RabbitConfigKombu


exchange = Exchange(
    RabbitConfigKombu.exchange.value,
    RabbitConfigKombu.exchange_type.value,
)

broker_scheme = BrokerScheme(Queue(RabbitConfigKombu.queue.value, exchange))
