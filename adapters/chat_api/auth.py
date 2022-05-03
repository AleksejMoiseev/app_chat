import falcon
from classic.components.component import component
from falcon import Request, Response
from classic.aspects import points

from application.dataclases import User
from application.serializer import UserSerializer
from application.services import UserService
from core.jwt import get_jwt_token, get_jwt_by_payload


@component
class RegisterUser:
    user_service: UserService

    @points.join_point
    def on_post_register(self, req: Request, resp: Response):
        data = req.get_media()
        email = data.get('email')
        password = data.get('password')
        if not (email and password):
            raise falcon.HTTPUnauthorized(description='The request must contain a login and password')
        username = data.get('username') or email
        serializer_data = UserSerializer(username=username, email=email, password=password)
        cleaned_data = serializer_data.cleaned_data
        user = User(**cleaned_data)
        user = self.user_service.register(user)
        user.refresh_token, _ = get_jwt_token()
        user.access_token = get_jwt_by_payload({'sub': user.id, 'preferred_username': user.email, 'name': user.username})
        resp.status = falcon.HTTP_200
        resp.body = {
            'id': user.id,
            'username': user.username,
            'refresh_token': user.refresh_token,
            'access_token': user.access_token
        }

    def on_post_login(self, req, resp):
        data = req.get_media()
        serializer_data = UserSerializer(**data)
        cleaned_data = serializer_data.cleaned_data
        user = self.user_service.filer_by(cleaned_data)

        if not user:
            resp.body = {
                "refresh_token": None,
                "access_token": None,
            }
            resp.status = falcon.HTTP_404
        else:
            user.refresh_token, _ = get_jwt_token()
            user.access_token = get_jwt_by_payload({'id': user.id})
            resp.body = {
                "refresh_token": user.refresh_token,
                "access_token": user.access_token,
            }
            resp.status = falcon.HTTP_200
