from gevent import monkey, pywsgi  # import the monkey for some patching as well as the WSGI server
monkey.patch_all()  # make sure to do the monkey-patching before loading the falcon package!
import falcon  # once the patching is done, we can load the Falcon package


class Handler:  # create a basic handler class with methods to deal with HTTP GET, PUT, and DELETE methods
    def on_get(self, request, response):
        response.status = falcon.HTTP_200
        response.content_type = "application/json"
        response.body = '{"message": "HTTP GET method used"}'

    def on_post(self, request, response):
        response.status = falcon.HTTP_404
        response.content_type = "application/json"
        response.body = '{"message": "POST method is not supported"}'

    def on_put(self, request, response):
        response.status = falcon.HTTP_200
        response.content_type = "application/json"
        response.body = '{"message": "HTTP PUT method used"}'

    def on_delete(self, request, response):
        response.status = falcon.HTTP_200
        response.content_type = "application/json"
        response.body = '{"message": "HTTP DELETE method used"}'


api = falcon.API()
api.add_route("/test", Handler())  # set the handler for dealing with HTTP methods; you may want add_sink for a catch-all
# port = 8080
# server = pywsgi.WSGIServer(("localhost", port), api)  # address and port to bind, and the Falcon handler API
# server.serve_forever()  # once the server is created, let it serve forever

if __name__ == '__main__':
    server = pywsgi.WSGIServer(("localhost", 8080), api)  # address and port to bind, and the Falcon handler API
    server.serve_forever()  # once the server is created, let it serve forever
