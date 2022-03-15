import base64
import re

from pydantic.annotated_types import Any

from core.serializer import ModelSerializer
from pydantic import validator

from users.exceptions import EmailError


class UserSerializer(ModelSerializer):
    username: str
    email: str
    password: Any

    @staticmethod
    def __encode_password(value: str):
        value = value.encode('utf-8')
        return base64.b64encode(value)

    @staticmethod
    def __decode_password(value):
        return base64.b64decode(value).decode('utf-8')

    @validator('username')
    def clean_username(cls, value: str):
        return value.capitalize()

    @validator('email')
    def clean_email(cls, value: str):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, value):
            return value
        raise EmailError()

    @validator('password')
    def clean_password(cls, value: str):
        return cls.__encode_password(value)






if __name__ == '__main__':
    user = UserSerializer(name='Alex')
    print(user.cleaned_data)