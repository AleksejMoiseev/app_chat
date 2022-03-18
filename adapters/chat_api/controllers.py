import falcon
from falcon import Request, Response

from application.dto import Message, Chat, ChatMember
from application.errors import BadRequest
from application.services import (

    ChatsChange, MessageValidator, ChatMemberValidator
)
from composites.chat_api import chat_app


class Chats:
    """Создание чата"""

    def on_post(self, req: Request, resp: Response):
        user = req.context.user
        data = req.get_media()
        chat = Chat(owner=user.pk, **data)
        chat = chat_app.create_chat(chat)
        resp.body = chat.dict()
        resp.status = falcon.HTTP_201


class ChangeChats:
    """Update and delete chat"""

    def on_put(self, req: Request, resp: Response, chat_id):
        params = req.get_media()
        change_chat = ChatsChange(pk=chat_id, **params)
        chat = chat_app.get_chat(change_chat.pk)
        if not chat:
            raise BadRequest()
        owner = req.context.user
        if not chat_app.is_owner(owner, chat):
            raise BadRequest()
        cleaned_data = change_chat.dict()
        for field, value in cleaned_data.items():
            if value is None:
                continue
            setattr(chat, field, value)
        resp.body = chat.dict()
        resp.status = falcon.HTTP_200

    def on_patch(self, req: Request, resp: Response, chat_id):
        return self.on_put(req, resp, chat_id)

    def on_delete(self, req: Request, resp: Response, chat_id):
        owner = req.context.user
        change_chat = ChatsChange(pk=chat_id)
        chat = chat_app.get_chat(change_chat.pk)
        if not chat_app.is_owner(owner, chat):
            raise BadRequest()
        deleted_chat = chat_app.delete_chat(chat.pk)
        resp.body = deleted_chat.dict()
        resp.status = falcon.HTTP_200


class GetChatInfoMembers:

    def on_get(self, req: Request, resp: Response, chat_id):
        user = req.context.user
        change_chat = ChatsChange(pk=chat_id)
        chat = chat_app.get_chat(change_chat.pk)
        if not chat:
            raise BadRequest()
        if not chat_app.is_member(user.pk, chat.pk):
            raise BadRequest()
        resp.body = chat.dict()
        resp.status = falcon.HTTP_200


class GetAllMembers:

    def on_get(self, req: Request, resp: Response, chat_id):
        user = req.context.user
        change_chat = ChatsChange(pk=chat_id)
        chat = chat_app.get_chat(change_chat.pk)
        if not chat_app.is_member(user.pk, chat.pk):
            raise BadRequest()
        members = chat_app.get_members_by_chat(chat.pk)
        resp.body = {
            'members': members,
        }
        resp.status = falcon.HTTP_200


class ListMessages:

    def on_get(self, req: Request, resp: Response, chat_id):
        limit = req.get_param_as_int('limit')
        offset = req.get_param_as_int('offset')
        user = req.context.user
        change_chat = ChatsChange(pk=chat_id)
        chat = chat_app.get_chat(change_chat.pk)
        if not chat:
            raise BadRequest()
        if not chat_app.is_member(user.pk, chat.pk):
            raise BadRequest()
        messages = chat_app.get_messages_by_chat_id(
            user_id=user.pk,
            chat_id=change_chat.pk,
            limit=limit,
            offset=offset
        )
        resp.body = {
            'messages': messages
        }
        resp.status = falcon.HTTP_200


class CreateMessage:
    def on_post(self, req: Request, resp: Response):
        user = req.context.user
        params = req.get_media()
        message = MessageValidator(user_id=user.pk, **params)
        chat = chat_app.get_chat(message.chat_id)
        if not chat:
            raise BadRequest()

        if not chat_app.is_member(user.pk, chat.pk):
            raise BadRequest()

        message_cleaned_data = message.dict()
        message = Message(**message_cleaned_data)
        message_created = chat_app.send_message(message)
        resp.body = message_created.dict()
        resp.status = falcon.HTTP_201


class OwnerMemberDeleteADD:

    def on_post(self, req: Request, resp: Response):
        owner = req.context.user
        data = req.get_media()
        cleaned_data = ChatMemberValidator(**data).dict()
        chat_id = cleaned_data['chat_id']
        chat = chat_app.get_chat(chat_id)
        if not chat:
            raise BadRequest()
        if not chat_app.is_owner(owner, chat):
            raise BadRequest()
        member = ChatMember(**cleaned_data)
        member = chat_app.add_member_to_chat(member)
        resp.body = member.dict()
        resp.status = falcon.HTTP_201

    def on_delete(self, req: Request, resp: Response):
        """TODO: deleted member and testing"""
        owner = req.context.user
        data = req.get_media()
        cleaned_data = ChatMemberValidator(**data).dict()
        chat_id = cleaned_data['chat_id']
        chat = chat_app.get_chat(chat_id)
        if not chat:
            raise BadRequest()
        if not chat_app.is_owner(owner, chat):
            raise BadRequest()
        user_id = cleaned_data['user_id']
        chat_id = cleaned_data['chat_id']

        deleted_member = chat_app.delete_member(user_id=user_id, chat_id=chat_id)
        if not deleted_member:
            raise BadRequest()

        resp.body = deleted_member.dict()
        resp.status = falcon.HTTP_200