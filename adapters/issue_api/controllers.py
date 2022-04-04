import falcon
from classic.aspects import points
from classic.components.component import component
from falcon import Request, Response

from application.issue_aplication.errors import BadRequest
from application.issue_aplication.services import IssueUserService


@component
class IssueUsers:
    service: IssueUserService

    @points.join_point
    def on_post_create(self, req: Request, resp: Response):
        data = req.get_media()
        issue_user = self.service.create_issue(data)
        resp.body = issue_user
        resp.status = falcon.HTTP_201

    @points.join_point
    def on_post_update(self, req: Request, resp: Response):
        data = req.get_media()
        issue_user = self.service.update_issue(data)
        resp.body = issue_user
        resp.status = falcon.HTTP_200

    @points.join_point
    def on_post_delete(self, req: Request, resp: Response):
        data = req.get_media()
        result = self.service.delete_issue(data)
        resp.body = result
        resp.status = falcon.HTTP_200

    def on_get_list(self, req: Request, resp: Response):
        issue_users = self.service.get_issues()
        resp.body = issue_users
        resp.status = falcon.HTTP_200

    def on_get_one(self, req: Request, resp: Response):
        id = req.get_param_as_int('id')
        issue_user = self.service.get_issue(id)
        if not issue_user:
            raise BadRequest()
        resp.body = issue_user
        resp.status = falcon.HTTP_200
