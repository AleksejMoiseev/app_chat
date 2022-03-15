from abc import abstractmethod


class BaseModel:
    serializer = None

    def __init__(self):
        self.pk = None

    def __str__(self):
        return f"{self.pk}"
