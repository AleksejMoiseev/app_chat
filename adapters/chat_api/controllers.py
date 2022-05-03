import falcon
from classic.components.component import component
from falcon import Request, Response
from classic.aspects import points

from application.dataclases import Message, ChatMember
from application.errors import BadRequest
from application.services import ChatService
from application.interfaces import ServiceInterface
from application.services import (

    ChatsChange, MessageValidator, ChatMemberValidator, ChatMemberService, MessageService
)

from evraz.classic.http_auth import (
    authenticate,
    authenticator_needed,
    authorize,
)


@authenticator_needed
@component
class Chats:
    chat_service: ChatService
    user_service: ServiceInterface

    @points.join_point
    @authenticate
    def on_post_create(self, req: Request, resp: Response):
        user_id = req.context.client.user_id
        user = self.user_service.get_user(user_id)
        data = req.get_media()
        chat = self.chat_service.create_chat(user, data)
        resp.body = chat
        resp.status = falcon.HTTP_201


@component
class ChangeChats:
    chat_service: ChatService
    chat_member_service: ChatMemberService

    @points.join_point
    def on_put_update(self, req: Request, resp: Response):
        params = req.get_media()
        change_chat = ChatsChange(**params)
        owner = req.context.user
        chat_id = change_chat.id
        chat = self.chat_service.get_chat_by_owner(owner, chat_id)
        print(self.chat_member_service.is_member(user=owner, chat=chat))
        cleaned_data = {key: value for key, value in change_chat.dict().items() if value is not None and key != 'id'}
        self.chat_service.update_chat(chat_id, cleaned_data)
        resp.body = chat
        resp.status = falcon.HTTP_200

    @points.join_point
    def on_put_delete_chat(self, req: Request, resp: Response):
        owner = req.context.user
        params = req.get_media()
        change_chat = ChatsChange(**params)
        chat_id = change_chat.id
        chat = self.chat_service.get_chat_by_owner(owner, chat_id)
        deleted_chat = self.chat_service.delete_chat(chat_id)
        if not deleted_chat:
            raise BadRequest()
        resp.body = chat
        resp.status = falcon.HTTP_200

    @points.join_point
    def on_post_add_member(self, req: Request, resp: Response):
        owner = req.context.user
        data = req.get_media()
        cleaned_data = ChatMemberValidator(**data).dict()
        chat_id = cleaned_data['chat_id']
        chat = self.chat_service.get_chat_by_owner(owner, chat_id)
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

    @points.join_point
    def on_delete_delete_member(self, req: Request, resp: Response):
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

    def on_get_info(self, req: Request, resp: Response):
        chat_id = req.get_param_as_int('chat_id')
        user = req.context.user
        change_chat = ChatsChange(id=chat_id)
        chat_id = change_chat.id
        chat = self.chat_service.get_chat(chat_id)
        is_member = self.chat_member_service.is_member(user=user, chat=chat)

        if is_member:
            resp.body = chat
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_400

    def on_get_members(self, req: Request, resp: Response):
        chat_id = req.get_param_as_int('chat_id')
        user = req.context.user
        change_chat = ChatsChange(id=chat_id)
        chat = self.chat_service.get_chat(change_chat.id)
        is_member = self.chat_member_service.is_member(user=user, chat=chat)
        if not is_member:
            raise BadRequest()
        members = self.chat_member_service.get_members_by_chat(chat)
        resp.body = members
        resp.status = falcon.HTTP_200

    @points.join_point
    def on_post_leave(self, req: Request, resp: Response):
        user = req.context.user
        params = req.get_media()
        change_chat = ChatsChange(**params)
        chat_id = change_chat.id
        chat = self.chat_service.get_chat(chat_id)
        if not chat:
            raise BadRequest()
        is_member = self.chat_member_service.is_member(user=user, chat=chat)
        member_by_user = self.chat_member_service.get_member(user.pk)
        pass


@component
class ListMessages:
    chat_service: ChatService
    chat_member_service: ChatMemberService
    message_service: MessageService

    def on_get_list(self, req: Request, resp: Response):
        chat_id = req.get_param_as_int('chat_id')
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

    @points.join_point
    def on_post_create(self, req: Request, resp: Response):
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
