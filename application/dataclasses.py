from pydantic import BaseModel as DTO


class BaseModel(DTO):
   pk: int