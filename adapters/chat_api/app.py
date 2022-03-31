from classic.http_api import App
from pydantic import ValidationError

from adapters.chat_api import controllers
from adapters.chat_api import auth
from adapters.chat_api.utils.middleware import JSONTranslator, JWTUserAuthMiddleware
from application import services
from application.errors import handle, BadRequest


def create_app(
    chat_service: services.ChatService,
    user_service: services.UserService,
    message_service: services.MessageService,
    chat_member_service: services.ChatMemberService,
) -> App:
    middleware = [
        JSONTranslator(),
        JWTUserAuthMiddleware(user_service=user_service),

    ]

    app = App(middleware=middleware, prefix='/api')
    app.register(controllers.Chats(chat_service=chat_service))
    app.register(controllers.ChangeChats(chat_service=chat_service, chat_member_service=chat_member_service))
    app.register(controllers.ListMessages(
        chat_service=chat_service,
        chat_member_service=chat_member_service,
        message_service=message_service
    ))
    app.register(auth.RegisterUser(
        user_service=user_service,
    ))
    app.add_error_handler(ValidationError, handle)
    app.add_error_handler(BadRequest)
    return app