from classic.app.dto import DTO
from classic.components.component import component
from classic.messaging import Message
from classic.messaging import Publisher

from adapters.message_bus.settings import ExchangeTopic
from application.issue_aplication.dataclases import IssueUser
from application.issue_aplication.interfaces import IssueRepositoryInterface


class IssueDTO(DTO):
    user: int
    status: bool


class ChangeIssueUser(DTO):
    id: int
    user: int = None
    status: bool = None


@component
class IssueUserService:
    _repository: IssueRepositoryInterface
    publisher: Publisher

    def _send_message(self, body: dict):
        message = {'message': body}
        self.publisher.plan(
            Message(ExchangeTopic.exchange.value, message)
        )

    def register(self, issue: IssueUser):
        issue = self._repository.add(issue)
        return issue

    def create_issue(self, data):
        issue_dto = IssueDTO(**data)
        cleaned_data = issue_dto.dict()
        issue = IssueUser(**cleaned_data)
        return self.register(issue)

    def get_issue(self, pk):
        issue = self._repository.get(pk)
        return issue

    def get_issues(self, limit=None, offset=None, **params):
        issues = self._repository.get_list(limit=limit, offset=offset, **params)
        return issues

    @staticmethod
    def cleaned_data(data, model=ChangeIssueUser):
        validate_data = model(**data)
        cleaned_data = validate_data.dict()
        return cleaned_data

    def delete_issue(self, data):
        cleaned_data = self.cleaned_data(data=data)
        id = cleaned_data['id']
        return self._repository.delete(id)

    def update_issue(self, data):
        cleaned_data = self.cleaned_data(data=data)
        id = cleaned_data['id']
        prepare_data = {
            key: value for key, value in cleaned_data.items() if value is not None and key != 'id'
        }
        return self._repository.update(reference=id, params=prepare_data)
