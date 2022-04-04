import falcon
from classic.aspects import points
from classic.components.component import component
from falcon import Request, Response
from application.user_application.services import UserService
from application.user_application.services import UserDTO
from application.user_application.dataclases import User


@component
class Users:
    user_service: UserService

    @points.join_point
    def on_post_create(self, req: Request, resp: Response):
        data = req.get_media()
        user_dto = UserDTO(**data)
        cleaned_data = user_dto.dict()
        print('@@@@@@222', cleaned_data)
        user = User(**cleaned_data)
        new_user = self.user_service.register(user)
        print('@@@@@@', new_user)
        resp.status = falcon.HTTP_200

    @points.join_point
    def on_post_update(self, req: Request, resp: Response):
        data = req.get_media()

    @points.join_point
    def on_post_delete(self, req: Request, resp: Response):
        data = req.get_media()

    def on_get_list(self, req: Request, resp: Response):
        pass

    def on_get_one(self, req: Request, resp: Response):
        pass

