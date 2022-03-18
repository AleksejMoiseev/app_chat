import datetime
import json
import re

import falcon
from falcon import Request, Response

from application.dto import Model
from composites.services import user_service
from core.auth_conf import jwt_skip_rules
from core.jwt import is_valid_access_token, get_decode_jwt_by_payload
from core.utils import validate_data


def _get_duration_components(duration):
    days = duration.days
    seconds = duration.seconds
    microseconds = duration.microseconds

    minutes = seconds // 60
    seconds = seconds % 60

    hours = minutes // 60
    minutes = minutes % 60

    return days, hours, minutes, seconds, microseconds


def duration_iso_string(duration):
    if duration < datetime.timedelta(0):
        sign = '-'
        duration *= -1
    else:
        sign = ''

    days, hours, minutes, seconds, microseconds = _get_duration_components(duration)
    ms = '.{:06d}'.format(microseconds) if microseconds else ""
    return '{}P{}DT{:02d}H{:02d}M{:02d}{}S'.format(sign, days, hours, minutes, seconds, ms)


class DjangoJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time
    """
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, datetime.timedelta):
            return duration_iso_string(o)
        else:
            return super().default(o)


class ChatSerializer(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Model):
            return o.dict()
        return super().default(o)


class JSONTranslator:

    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Content-Type', 'application/json')
        resp.body = json.dumps(resp.body, cls=ChatSerializer)


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
        payload = get_decode_jwt_by_payload(token) or None
        user = user_service.get_user(payload['pk'])
        if not user:
            raise falcon.HTTPUnauthorized(description='Invalid headers token')
        req.context.user = user_service.get_user(payload['pk'])





