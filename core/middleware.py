import json
import re

import falcon
from falcon import Request, Response

from core.auth_conf import jwt_skip_rules
from core.jwt import is_valid_access_token
from core.serializer import BaseSerializer
from core.utils import validate_data


class JSONTranslator:

    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Content-Type', 'application/json')
        resp.body = json.dumps(resp.body,cls=BaseSerializer)


def check_excluded_rules(method, path, config):
    for method_rule, path_rule in config:
        path_rule = path_rule.replace('*', '.+') + "[/]?$"
        if method == method_rule and re.match(path_rule.replace('*', '.+'), path):
            break
    else:
        return False
    return True


class JWTUserAuthMiddleware:

    def process_resource(self, req: Request, resp: Response, resource, params):
        if check_excluded_rules(method=req.method, path=req.path, config=jwt_skip_rules):
            return
        data = req.get_header("Authorization", required=True).split(' ')
        token_auth = validate_data(data)
        token = token_auth["value"]
        if not is_valid_access_token(token):
            raise falcon.HTTPUnauthorized(description='Invalid headers token')


