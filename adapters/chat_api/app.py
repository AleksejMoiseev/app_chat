from classic.http_api import App
from adapters.chat_api import controllers
from adapters.chat_api.utils.middleware import JSONTranslator, JWTUserAuthMiddleware
from application import services



def create_app(
    chat_service: services.ChatService,
    # checkout: services.UserService,
    # orders: services.MessageService,
    # customers: services.ChatMemberService,
) -> App:
    middleware = [
        JSONTranslator(),
        JWTUserAuthMiddleware(),

    ]

    app = App(middleware=middleware, prefix='/api')

    app.register(controllers.Chats(chat_service=chat_service))
    return app