import falcon
from classic.aspects import points
from classic.components.component import component
from falcon import Request, Response

from application.book_aplication.errors import BadRequest
from application.book_aplication.services import BookService


@component
class Books:
    service: BookService

    @points.join_point
    def on_post_create(self, req: Request, resp: Response):
        data = req.get_media()
        book = self.service.create_book(data)
        resp.body = book
        resp.status = falcon.HTTP_201

    @points.join_point
    def on_post_update(self, req: Request, resp: Response):
        data = req.get_media()
        book = self.service.update_book(data)
        resp.body = book
        resp.status = falcon.HTTP_200

    @points.join_point
    def on_post_delete(self, req: Request, resp: Response):
        data = req.get_media()
        result = self.service.delete_book(data)
        resp.body = result
        resp.status = falcon.HTTP_200

    def on_get_list(self, req: Request, resp: Response):
        books = self.service.get_books()
        resp.body = books
        resp.status = falcon.HTTP_200

    def on_get_one(self, req: Request, resp: Response):
        id = req.get_param_as_int('id')
        book = self.service.get_book(id)
        if not book:
            raise BadRequest()
        resp.body = book
        resp.status = falcon.HTTP_200
