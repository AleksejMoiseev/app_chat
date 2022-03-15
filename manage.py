from gevent import monkey, pywsgi  # import the monkey for some patching as well as the WSGI server
monkey.patch_all()  # make sure to do the monkey-patching before loading the falcon package!
import falcon  # once the patching is done, we can load the Falcon package
from core.middleware import JSONTranslator
from users.views import RegisterUser, AuthView
from users.exceptions import EmailError


middleware = [
    JSONTranslator(),
    #JWTUserAuthMiddleware(),

]


api = falcon.API(middleware=middleware)

"""Exceptions"""
api.add_error_handler(EmailError)


"""URLS"""
api.add_route("/register", RegisterUser())
api.add_route("/login", AuthView())



# port = 8080
# server = pywsgi.WSGIServer(("localhost", port), api)  # address and port to bind, and the Falcon handler API
# server.serve_forever()  # once the server is created, let it serve forever

if __name__ == '__main__':
    server = pywsgi.WSGIServer(("localhost", 8080), api)  # address and port to bind, and the Falcon handler API
    server.serve_forever()  # once the server is created, let it serve forever
