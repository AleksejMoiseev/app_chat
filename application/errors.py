import falcon


class BadRequest(Exception):
    @staticmethod
    def handle(req, resp, exc, params):
        resp.set_header("X-Custom-Header", "*")
        resp.body = f"Parameters in a request cannot be validated"
        resp.status = falcon.HTTP_404
