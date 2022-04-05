import falcon
from classic.aspects import points
from classic.components.component import component
from falcon import Request, Response

from application.user_application.errors import BadRequest
from application.user_application.services import UserService


@component
class Users:
    user_service: UserService

    @points.join_point
    def on_post_create(self, req: Request, resp: Response):
        data = req.get_media()
        user = self.user_service.create_user(data)
        resp.body = user
        resp.status = falcon.HTTP_201

    @points.join_point
    def on_post_update(self, req: Request, resp: Response):
        data = req.get_media()
        user = self.user_service.update_user(data)
        resp.body = user
        resp.status = falcon.HTTP_200

    @points.join_point
    def on_post_delete(self, req: Request, resp: Response):
        data = req.get_media()
        result = self.user_service.delete_user(data)
        resp.body = result
        resp.status = falcon.HTTP_200

    @points.join_point
    def on_get_list(self, req: Request, resp: Response):
        users = self.user_service.get_users()
        resp.body = users
        resp.status = falcon.HTTP_200

    @points.join_point
    def on_get_one(self, req: Request, resp: Response):
        id = req.get_param_as_int('id')
        user = self.user_service.get_user(id)
        if not user:
            raise BadRequest()
        resp.body = user
        resp.status = falcon.HTTP_200
