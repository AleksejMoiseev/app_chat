from typing import List

from pydantic import ValidationError
import falcon

from application.dto import User, Message, Chat, ChatMember
from application.errors import ParamsIsNotValid
from application.services import (
    ChatMemberService, ChatService, MessageService,
    chat_service, chat_member_service, message_service,
    user_service
)
from datetime import datetime
from falcon import Request, Response


class ChatInteractor:
    def __init__(self, chat_member: ChatMemberService, chat: ChatService, message: MessageService,):
        self.chat_member = chat_member
        self.chat = chat
        self.message = message
        self.user = user_service

    def create_chat(self, chat: Chat):
        chat = self.chat.create_chat(chat)
        params = {
            "user_id": chat.owner,
            "chat_id": chat.pk,
        }
        chat_member = ChatMember(**params)
        self.chat_member.create_members(chat_member)
        return chat

    def past_message(self, interval: datetime, chat_id: int):
        pass

    def send_message(self, message: Message):
        return self.message.send_message(message)

    def get_members_by_chat(self, chat_id):
        pass

    def get_user(self, pk):
        return self.user.get_user(pk)

    def add_member_to_chat(self, user_id, chat_id):
        chat_member = ChatMember(user_id=user_id, chat_id=chat_id)
        return self.chat_member.create_members(chat_member)

    def get_chat(self, chat_id):
        return self.chat.get_chat(chat_id)

    def get_chats(self):
        return self.chat.get_chats()

    def get_members(self):
        return self.chat_member.get_members()


chat_app = ChatInteractor(
    chat_member=chat_member_service,
    chat=chat_service,
    message=message_service,
)


class Chats:

    def on_post_create_chat(self, req: Request, resp: Response):
        user = req.context.user
        data = req.get_media()
        chat = Chat(owner=user.pk, **data)
        chat = chat_app.create_chat(chat)
        resp.body = {'chat': chat.pk}
        resp.status = falcon.HTTP_201

    def on_get_message(self, req: Request, resp: Response):
        pass


class OwnerMemberCreate:

    def on_post_add_member(self, req: Request, resp: Response):
        owner = req.context.user
        data = req.get_media()
        chat_id = data['chat_id']
        chat = chat_app.get_chat(chat_id)
        if chat.owner == owner.pk:
            chat_member = chat_app.add_member_to_chat(**data)
            resp.body = {'pk': chat_member.pk}
            resp.status = falcon.HTTP_201
        else:
            resp.body = {'pk': None}
            resp.status = falcon.HTTPBadRequest


class OwnerMemberDelete:

    def on_path_member(self, req: Request, resp: Response):
        """TODO: owner"""
        owner = req.context.user
        data = req.get_media()
        member = ChatMember(**data)
        for chat_member in chat_app.get_members():
            condition = all(
                chat_member.user_id == member.user_id
                and chat_member.chat_id == member.chat_id
                and not chat_member.kicked
            )
            if condition:
                chat_member.kicked = datetime.now()
                resp.body = f"member{chat_member.pk} delete success"
                resp.status = falcon.HTTP_200































if __name__ == '__main__':
    parametr = {
        "title": "My_chat",
        "descriptions": "My descriptions",
        "owner_id": 0,
    }
    chat = Chat(**parametr)
    print(chat_app.create_chat(chat=chat))
    print(chat.created)