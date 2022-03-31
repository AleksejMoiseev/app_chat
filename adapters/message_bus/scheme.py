from classic.messaging_kombu import BrokerScheme
from kombu import Exchange, Queue
from adapters.message_bus.settings import ExchangeTopic


exchange = Exchange(
    ExchangeTopic.exchange.value,
    ExchangeTopic.exchange_type.value,
)

broker_scheme = BrokerScheme(Queue(ExchangeTopic.queue.value, exchange))
