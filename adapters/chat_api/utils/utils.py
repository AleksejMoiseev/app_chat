import falcon

from adapters.chat_api.utils.jwt import BEARER


def validate_data(data):
    if not (data[0] == BEARER and len(data) == 2):
        raise falcon.HTTPUnauthorized(description='Data is not valid')
    return {
        "name": data[0],
        "value": data[1]
    }