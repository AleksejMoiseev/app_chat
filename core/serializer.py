import json
from typing import List

from pydantic import BaseModel


class BaseSerializer(json.JSONEncoder):
    pass
    # def default(self, o):
    #     if isinstance(o, Base):
    #         return str(o.name)
    #     return super().default(o)


class ModelSerializer(BaseModel):
    """
    TODO: we will implement methods: is_valid(), clean(), clean_`fields`
    """
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

