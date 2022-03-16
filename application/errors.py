import falcon


class EmailError(Exception):
    @staticmethod
    def handle(req, resp, exc, params):
        resp.set_header("X-Custom-Header", "*")
        resp.body = f"Entity Not Found"
        resp.status = falcon.HTTP_404