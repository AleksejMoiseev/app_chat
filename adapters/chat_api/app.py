from classic.http_api import App
from pydantic import ValidationError
from evraz.classic.http_auth import Authenticator
import falcon

from adapters.chat_api import controllers
from adapters.chat_api import auth
from adapters.chat_api.utils.middleware import JSONTranslator, JWTUserAuthMiddleware
from application import services
from application.errors import handle, BadRequest

from evraz.classic.http_auth import Group, Permission, strategies
from evraz.classic.http_auth import strategies as auth_strategies


class Permissions:
    FULL_CONTROL = Permission('full_control')


class Groups:
    ADMINS = Group('admins', permissions=(Permissions.FULL_CONTROL, ))


dummy_strategy = strategies.Dummy(
    user_id=1,
    login='dummy',
    name='Admin dummy',
    groups=(Groups.ADMINS.name, ),
)

ALL_GROUPS = (Groups.ADMINS, )


def create_app(
    chat_service: services.ChatService,
    user_service: services.UserService,
    message_service: services.MessageService,
    chat_member_service: services.ChatMemberService,
) -> App:
    authenticator = Authenticator(app_groups=ALL_GROUPS)

    cors_middleware = falcon.CORSMiddleware(allow_origins='*')
    authenticator.set_strategies(auth_strategies.KeycloakOpenId())

    middleware = [
        JSONTranslator(),
        cors_middleware
    ]

    app = App(middleware=middleware, prefix='/api')
    app.register(controllers.Chats(authenticator=authenticator, chat_service=chat_service,user_service=user_service ))
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