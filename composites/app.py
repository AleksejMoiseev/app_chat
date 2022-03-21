from adapters.chat_api import app
from composites.chat_api import chat_service

app = app.create_app(
    chat_service=chat_service,

)