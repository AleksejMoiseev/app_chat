from core.service_interfaces import ServiceInterface
from core.storage import PythonStructRepository

table_chat = PythonStructRepository("chats")


class ChatService(ServiceInterface):
    pass


CHAT_ORM = ChatService(repository=table_chat)
