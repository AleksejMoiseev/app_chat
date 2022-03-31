import jwt
import datetime
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError


JWT_PARAMETERS = {
    "lifetime": {'days': 1},
    "key_refresh_token": "refresh_token",
    "key_access_token": "access_token",
    "algorithms": "HS256",
}


BEARER = "Bearer"


def get_jwt_token():
    lifetime_tokens = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(**JWT_PARAMETERS["lifetime"])

    refresh_token = jwt.encode(
        {"exp": lifetime_tokens},
        key=JWT_PARAMETERS["key_refresh_token"],
        algorithm=JWT_PARAMETERS["algorithms"],
    )

    access_token = jwt.encode(
        {"exp": lifetime_tokens},
        key=JWT_PARAMETERS["key_access_token"],
        algorithm=JWT_PARAMETERS["algorithms"],
    )
    return refresh_token, access_token


def is_valid_refresh_token(token):
    try:
        jwt.decode(
            token,
            key=JWT_PARAMETERS["key_refresh_token"],
            algorithms=[JWT_PARAMETERS["algorithms"], ]
        )
    except (ExpiredSignatureError, InvalidSignatureError):
        return False
    return True


def is_valid_access_token(token):
    try:
        jwt.decode(
            token,
            key=JWT_PARAMETERS["key_access_token"],
            algorithms=[JWT_PARAMETERS["algorithms"], ]
        )
    except (ExpiredSignatureError, InvalidSignatureError):
        return False
    return True