from adapters.chat_api import app
from composites.chat_api import (
    chat_service, message_service, chat_member_service,
    user_service
)

app = app.create_app(
    chat_service=chat_service,
    message_service=message_service,
    chat_member_service=chat_member_service,
    user_service=user_service
)