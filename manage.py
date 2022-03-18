from gevent import monkey, pywsgi  # import the monkey for some patching as well as the WSGI server

from adapters.chat_api.controllers import Chats, ChangeChats, GetAllMembers, ListMessages, \
    CreateMessage, GetChatInfoMembers, OwnerMemberDeleteADD
from application.errors import BadRequest

monkey.patch_all()  # make sure to do the monkey-patching before loading the falcon package!
import falcon  # once the patching is done, we can load the Falcon package
from adapters.chat_api.utils.middleware import JSONTranslator
from adapters.chat_api.auth import RegisterUser, AuthView
from pydantic import ValidationError
from adapters.chat_api.utils.middleware import JWTUserAuthMiddleware

middleware = [
    JSONTranslator(),
    JWTUserAuthMiddleware(),

]


def handle(req, resp, ex, params):
    raise falcon.HTTPError(falcon.falcon.HTTP_792)


api = falcon.API(middleware=middleware)

"""Exceptions"""
api.add_error_handler(ValidationError, handle)
api.add_error_handler(BadRequest)




"""URLS"""
api.add_route("/register", RegisterUser())
api.add_route("/login", AuthView())
api.add_route("/chats", Chats())
api.add_route("/chats/{chat_id}", ChangeChats())
api.add_route("/info/{chat_id}", GetChatInfoMembers())
api.add_route("/members/{chat_id}", GetAllMembers())
api.add_route("/messages/{chat_id}", ListMessages())
api.add_route("/messages", CreateMessage())
api.add_route("/members", OwnerMemberDeleteADD())



# port = 8080
# server = pywsgi.WSGIServer(("localhost", port), api)  # address and port to bind, and the Falcon handler API
# server.serve_forever()  # once the server is created, let it serve forever

if __name__ == '__main__':
    server = pywsgi.WSGIServer(("localhost", 8080), api)  # address and port to bind, and the Falcon handler API
    server.serve_forever()  # once the server is created, let it serve forever
