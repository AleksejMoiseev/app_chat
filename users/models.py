from core.models import BaseModel
from users.serializer import UserSerializer


class User(BaseModel):
    serializer = UserSerializer

    def __init__(self, username, email, password):
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
        self.access_token = None
        self.refresh_token = None

    @classmethod
    def user_serializer(cls, list_positions_values):
        return cls.serializer.serializer_data(data=list_positions_values)

    def check_password(self, value):
        return self.password == UserSerializer


if __name__ == '__main__':
    values = ['Alex', 'alex@mail.ru', "qqqqq"]
    params = {'username': "Alex", 'email': 'alex@mail.ru', 'password': "qqqqq"}
    #print(User.serializer.serializer_data(['Alex']))
    serializer_data = User.user_serializer(list_positions_values=values)
    print(serializer_data.cleaned_data)
    print(User.serializer(**params))
