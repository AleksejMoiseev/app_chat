import falcon
from classic.components.component import component
from falcon import Request, Response

from application.dto import Message, Chat, ChatMember
from application.errors import BadRequest
from application.services import ChatService
from application.services import (

    ChatsChange, MessageValidator, ChatMemberValidator, ChatMemberService, MessageService
)


@component
class Chats:
    chat_service: ChatService

    def on_post_create(self, req: Request, resp: Response):
        user = req.context.user
        data = req.get_media()
        chat = Chat(owner=user.pk, **data)
        chat = self.chat_service.create_chat(chat)
        resp.body = chat.dict()
        resp.status = falcon.HTTP_201


@component
class ChangeChats:
    chat_service: ChatService
    chat_member_service: ChatMemberService

    def on_put_update(self, req: Request, resp: Response):
        params = req.get_media()
        change_chat = ChatsChange(**params)
        chat = self.chat_service.get_chat(change_chat.pk)
        if not chat:
            raise BadRequest()
        owner = req.context.user
        if not self.chat_member_service.is_owner(owner, chat):
            raise BadRequest()
        cleaned_data = change_chat.dict()
        for field, value in cleaned_data.items():
            if value is None:
                continue
            setattr(chat, field, value)
        resp.body = chat.dict()
        resp.status = falcon.HTTP_200

    def on_put_delete_chat(self, req: Request, resp: Response):
        owner = req.context.user
        params = req.get_media()
        change_chat = ChatsChange(**params)
        chat = self.chat_service.get_chat(change_chat.pk)
        if not chat:
            raise BadRequest()
        if not self.chat_member_service.is_owner(owner, chat):
            raise BadRequest()
        deleted_chat = self.chat_service.delete_chat(chat.pk)
        resp.body = deleted_chat.dict()
        resp.status = falcon.HTTP_200


@component
class GetChatInfoMembers:
    chat_service: ChatService
    chat_member_service: ChatMemberService

    def on_get(self, req: Request, resp: Response, chat_id):
        user = req.context.user
        change_chat = ChatsChange(pk=chat_id)
        chat = self.chat_service.get_chat(change_chat.pk)
        if not chat:
            raise BadRequest()
        if not self.chat_member_service.is_member(user.pk, chat.pk):
            raise BadRequest()
        resp.body = chat.dict()
        resp.status = falcon.HTTP_200


@component
class GetAllMembers:
    chat_service: ChatService
    chat_member_service: ChatMemberService

    def on_get(self, req: Request, resp: Response, chat_id):
        user = req.context.user
        change_chat = ChatsChange(pk=chat_id)
        chat = self.chat_service.get_chat(change_chat.pk)
        if not self.chat_member_service.is_member(user.pk, chat.pk):
            raise BadRequest()
        members = self.chat_member_service.get_members_by_chat(chat.pk)
        resp.body = {
            'members': members,
        }
        resp.status = falcon.HTTP_200


@component
class ListMessages:
    chat_service: ChatService
    chat_member_service: ChatMemberService
    message_service: MessageService

    def on_get(self, req: Request, resp: Response, chat_id):
        limit = req.get_param_as_int('limit')
        offset = req.get_param_as_int('offset')
        user = req.context.user
        change_chat = ChatsChange(pk=chat_id)
        chat = self.chat_service.get_chat(change_chat.pk)
        if not chat:
            raise BadRequest()
        if not self.chat_member_service.is_member(user.pk, chat.pk):
            raise BadRequest()
        messages = self.message_service.get_messages_by_chat_id(
            user_id=user.pk,
            chat_id=change_chat.pk,
            limit=limit,
            offset=offset
        )
        resp.body = {
            'messages': messages
        }
        resp.status = falcon.HTTP_200


@component
class CreateMessage:
    chat_service: ChatService
    chat_member_service: ChatMemberService
    message_service: MessageService

    def on_post(self, req: Request, resp: Response):
        user = req.context.user
        params = req.get_media()
        message = MessageValidator(user_id=user.pk, **params)
        chat = self.chat_service.get_chat(message.chat_id)
        if not chat:
            raise BadRequest()

        if not self.chat_member_service.is_member(user.pk, chat.pk):
            raise BadRequest()

        message_cleaned_data = message.dict()
        message = Message(**message_cleaned_data)
        message_created = self.message_service.send_message(message)
        resp.body = message_created.dict()
        resp.status = falcon.HTTP_201


@component
class OwnerMemberDeleteADD:
    chat_service: ChatService
    chat_member_service: ChatMemberService

    def on_post(self, req: Request, resp: Response):
        owner = req.context.user
        data = req.get_media()
        cleaned_data = ChatMemberValidator(**data).dict()
        chat_id = cleaned_data['chat_id']
        chat = self.chat_service.get_chat(chat_id)
        if not chat:
            raise BadRequest()
        if not self.chat_member_service.is_owner(owner, chat):
            raise BadRequest()
        member = ChatMember(**cleaned_data)
        members_by_chat = self.chat_member_service.get_members_by_chat(chat_id)
        for m in members_by_chat:
            if member.user_id == m.user_id:
                resp.body = m.dict()
                resp.status = falcon.HTTP_200
                break
        else:
            member = self.chat_member_service.add_member_to_chat(member)
            resp.body = member.dict()
            resp.status = falcon.HTTP_201

    def on_delete(self, req: Request, resp: Response):
        owner = req.context.user
        data = req.get_media()
        cleaned_data = ChatMemberValidator(**data).dict()
        chat_id = cleaned_data['chat_id']
        chat = self.chat_service.get_chat(chat_id)
        if not chat:
            raise BadRequest()
        if not self.chat_member_service.is_owner(owner, chat):
            raise BadRequest()
        user_id = cleaned_data['user_id']
        chat_id = cleaned_data['chat_id']

        deleted_member = self.chat_member_service.delete_member(user_id=user_id, chat_id=chat_id)
        if not deleted_member:
            raise BadRequest()

        resp.body = deleted_member.dict()
        resp.status = falcon.HTTP_200