from typing import List

from pydantic import ValidationError
import falcon

from application.dto import User, Message, Chat, ChatMember
from application.errors import ParamsIsNotValid
from application.services import (
    ChatMemberService, ChatService, MessageService,
    chat_service, chat_member_service, message_service,
    user_service, ChatsChange, MessageValidator
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

    def delete_chat(self, chat_id):
        return self.chat.delete_chat(chat_id)

    def past_message(self, interval: datetime, chat_id: int):
        pass

    def send_message(self, message: Message):
        return self.message.send_message(message)

    def get_messages_by_chat_id(self, user_id, chat_id):
        messages = self.message.get_messages()
        messages_body = []
        for message in messages:
            if message.chat_id == chat_id and message.user_id == user_id:
                messages_body.append(message.body)
        return messages_body



    def get_members_by_chat(self, chat_id):
        members_all = self.chat_member.get_members()
        members = []
        for member in members_all:
            if member.chat_id == chat_id:
                members.append(member.pk)
        return members

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

    @staticmethod
    def is_owner(owner: User, chat: Chat):
        if owner.pk == chat.owner:
            return True
        return False

    def is_member(self, member, chat):
        return self.is_owner(member, chat)


chat_app = ChatInteractor(
    chat_member=chat_member_service,
    chat=chat_service,
    message=message_service,
)


class Chats:
    """Создание чата"""

    def on_post(self, req: Request, resp: Response):
        user = req.context.user
        data = req.get_media()
        chat = Chat(owner=user.pk, **data)
        chat = chat_app.create_chat(chat)
        resp.body = {'chat': chat.pk}
        resp.status = falcon.HTTP_201

    def on_get_message(self, req: Request, resp: Response):
        pass


class ChangeChats:
    """Update and delete chat"""

    def on_put(self, req: Request, resp: Response, chat_id):
        params = req.get_media()
        change_chat = ChatsChange(pk=chat_id, **params)
        chat = chat_app.get_chat(change_chat.pk)
        if not chat:
            raise falcon.HTTPBadRequest()
        owner = req.context.user
        if not chat_app.is_owner(owner, chat):
            raise falcon.HTTPBadRequest()
        cleaned_data = change_chat.dict()
        for field in cleaned_data:
            value = cleaned_data[field]
            if not value:
                continue
            setattr(chat, field, value)
        resp.body = {'title': chat.title, 'descriptions': chat.descriptions}
        resp.status = falcon.HTTP_200

    def on_patch(self, req: Request, resp: Response, chat_id):
        return self.on_put(req, resp, chat_id)

    def on_delete(self, req: Request, resp: Response, chat_id):
        owner = req.context.user
        change_chat = ChatsChange(pk=chat_id)
        chat = chat_app.get_chat(change_chat.pk)
        if not chat_app.is_owner(owner, chat):
            raise falcon.HTTPInvalidParam(param_name='chat_id', msg='Do not belong')
        deleted_chat = chat_app.delete_chat(chat.pk)
        resp.body = {
            'deleted': 'success',
            'id': deleted_chat.pk
        }
        resp.status = falcon.HTTP_201


class ActionsMembers:

    def on_get(self, req: Request, resp: Response, chat_id):
        member = req.context.user
        change_chat = ChatsChange(pk=chat_id)
        chat = chat_app.get_chat(change_chat.pk)
        if not chat_app.is_member(member, chat):
            raise falcon.HTTPInvalidParam(param_name='chat_id', msg='Do not belong')
        resp.body = {
            'chat_info': [chat.title, chat.descriptions]
        }
        resp.status = falcon.HTTP_200


class GetAllMembers:

    def on_get(self, req: Request, resp: Response, chat_id):
        member = req.context.user
        change_chat = ChatsChange(pk=chat_id)
        chat = chat_app.get_chat(change_chat.pk)
        if not chat_app.is_member(member, chat):
            raise falcon.HTTPInvalidParam(param_name='chat_id', msg='Do not belong')
        members = chat_app.get_members_by_chat(chat.pk)
        resp.body = {
            'members': members,
        }
        resp.status = falcon.HTTP_200


class ListMessages:

    def on_get(self, req: Request, resp: Response, chat_id):
        member = req.context.user
        change_chat = ChatsChange(pk=chat_id)
        chat = chat_app.get_chat(change_chat.pk)
        if not chat_app.is_member(member, chat):
            raise falcon.HTTPInvalidParam(param_name='chat_id', msg='Do not belong')
        messages = chat_app.get_messages_by_chat_id(user_id=member.pk, chat_id=change_chat.pk)
        resp.body = {
            'messages': messages
        }
        resp.status = falcon.HTTP_200


class CreateMessage:
    def on_post(self, req: Request, resp: Response):
        member = req.context.user
        params = req.get_media()
        message = MessageValidator(user_id=member.pk, **params)
        chat = chat_app.get_chat(message.chat_id)

        if not chat:
            raise falcon.HTTPBadRequest()

        if not chat_app.is_member(member, chat):
            raise falcon.HTTPBadRequest()

        message_cleaned_data = message.dict()
        message = Message(**message_cleaned_data)
        message_created = chat_app.send_message(message)
        resp.body = {
            'id': message_created.pk,
            'message': message_created.body
        }
        resp.status = falcon.HTTP_201


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