import abc
from classic.components import component
from classic.aspects import PointCut
from pydantic import validate_arguments
from classic.http_api import App

from core.storage import RepositoryInterface


class ServiceInterface(abc.ABC):
    def __init__(self, repository: RepositoryInterface):
        self._repository = repository