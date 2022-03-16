import json
from typing import List

from pydantic import BaseModel


class ModelSerializer(BaseModel):

    @classmethod
    def key(cls):
        return tuple(cls.__fields__.keys())

    @property
    def cleaned_data(self):
        return self.dict()

    @classmethod
    def serializer_data(cls, data: List):
        data = tuple(data)
        params = dict(zip(cls.key(), data))
        return cls(**params)
