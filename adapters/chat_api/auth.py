import falcon
from falcon import Request, Response

from application.dto import User
from application.serializer import UserSerializer
from composites.chat_api import user_service
from core.jwt import get_jwt_token, is_valid_refresh_token, get_jwt_by_payload
from core.utils import validate_data


class RegisterUser:

    def on_post(self, req: Request, resp: Response):
        data = req.get_media()
        email = data.get('email')
        password = data.get('password')
        if not (email and password):
            raise falcon.HTTPUnauthorized(description='The request must contain a login and password')
        username = data.get('username') or email
        serializer_data = UserSerializer(username=username, email=email, password=password)
        cleaned_data = serializer_data.cleaned_data
        user = User(**cleaned_data)
        user = user_service.register(user)
        user.refresh_token, _ = get_jwt_token()
        user.access_token = get_jwt_by_payload({'pk': user.pk})
        resp.status = falcon.HTTP_200
        resp.body = {
            'pk': user.pk,
            'username': user.username,
            'refresh_token': user.refresh_token,
            'access_token': user.access_token
        }


class AuthView:

    def on_post(self, req, resp):
        """TODO: It is necessary to write a competent encoding of the payload tied for a while
         """
        data = req.get_media()
        email = data.get('email')
        password = data.get('password')
        if not (email and password):
            raise falcon.HTTPUnauthorized(description='The request must contain a login and password')
        username = data.get('username') or email
        serializer_data = UserSerializer(username=username, email=email, password=password)
        users = user_service.get_users()
        user = None
        for user in users:
            if user.email == serializer_data.email and user.password == serializer_data.password:
                user = user
                break

        if not user:
            resp.body = {
                "refresh_token": None,
                "access_token": None,
            }
            resp.status = falcon.HTTP_404
        else:
            user.refresh_token, user.access_token = get_jwt_token()
            resp.body = {
                "refresh_token": user.refresh_token,
                "access_token": user.access_token,
            }
            resp.status = falcon.HTTP_200

    def on_put(self, req, resp):
        """
        TODO implemented token decay by time need to add payload
        :param req:
        :param resp:
        :return:
        """
        data = req.get_header("Authorization").split(' ')
        token_auth = validate_data(data)
        token = token_auth["value"]
        if is_valid_refresh_token(token):
            refresh_token, access_token = get_jwt_token()
            resp.body = {
                "refresh_token": refresh_token,
                "access_token": access_token
            }
        else:
            raise falcon.HTTPUnauthorized(description='Incorrect refresh token')
