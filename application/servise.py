# from datetime import datetime
#
# from classic.app.dto import DTO
# from classic.components.component import component
#
# from application.dto import User, Message, Chat, ChatMember
# from composites.chat_api import message_storage, chat_storage, chat_member_storage
# from .interfaces import (
#     UserRepositoryInterface, MessageRepositoryInterface, ChatMembersRepositoryInterface,
#     ChatRepositoryInterface,
# )
#
#
# class ChatsChange(DTO):
#     pk: int
#     title: str = None
#     descriptions: str = None
#
#
# class MessageValidator(DTO):
#     user_id: int
#     chat_id: int
#     body: str = None
#
#
# class ChatMemberValidator(DTO):
#     user_id: int
#     chat_id: int
#     checked_out: datetime = None
#     kicked: datetime = None
#
#
# @component
# class UserService:
#     _repository: UserRepositoryInterface
#
#     def register(self, user: User):
#         user = self._repository.add(user)
#         return user
#
#     def get_user(self, pk):
#         user = self._repository.get(pk)
#         return user
#
#     def get_users(self, limit=None, offset=None, **params):
#         users = self._repository.get_list(limit=limit, offset=offset, **params)
#         return users
#
#
# @component
# class MessageService:
#     messages_repo: MessageRepositoryInterface
#
#     def send_message(self, message: Message):
#         message = self.messages_repo.add(message)
#         return message
#
#     def get_messages(self, limit=None, offset=None, **params):
#         messages = self.messages_repo.get_list(limit=limit, offset=offset, **params)
#         return messages
#
#     def get_messages_by_chat_id(self, user_id, chat_id, limit, offset):
#         chats_messages = self.get_messages(limit=limit, offset=offset)
#         messages = []
#         for message in chats_messages:
#             if message.chat_id == chat_id:
#                 messages.append(message)
#         return messages
#
#
# @component
# class ChatService:
#     chats_repo: ChatRepositoryInterface
#     members_repo: ChatMembersRepositoryInterface
#
#     def register_chat(self, chat: Chat):
#         chat = self.chats_repo.add(chat)
#         return chat
#
#     def create_chat(self, chat: Chat):
#         chat = self.register_chat(chat)
#         params = {
#             "user_id": chat.owner,
#             "chat_id": chat.pk,
#         }
#         chat_member = ChatMember(**params)
#         self.members_repo.add(chat_member)
#         return chat
#
#     def _delete_chat(self, pk):
#         return self.chats_repo.delete(pk)
#
#     def delete_chat(self, chat_id):
#         members = self.members_repo.get_list()
#         for member in members:
#             if member.chat_id == chat_id:
#                 member.kicked = datetime.now()
#         return self._delete_chat(chat_id)
#
#     def get_chat(self, pk):
#         chat = self.chats_repo.get(pk)
#         return chat
#
#     def get_chats(self, limit=None, offset=None, **params):
#         chats = self.chats_repo.get_list(limit=limit, offset=offset, **params)
#         return chats
#
#
# @component
# class ChatMemberService:
#     _repository: ChatMembersRepositoryInterface
#
#     def get_members(self, limit=None, offset=None, **params):
#         members = self._repository.get_list(limit=limit, offset=offset, **params)
#         return members
#
#     def create_members(self, chat_member: ChatMember):
#         chat_member = self._repository.add(chat_member)
#         return chat_member
#
#     def _get_member(self, pk):
#         return self._repository.get(pk)
#
#     def _delete_member(self, pk):
#         chat_member = self._repository.delete(pk)
#         return chat_member
#
#     def get_members_by_chat(self, chat_id):
#         members_all = self.get_members()
#         members = []
#         for member in members_all:
#             if member.chat_id == chat_id and not member.kicked:
#                 members.append(member)
#         return members
#
#     def get_member(self, user_id):
#         member = self._get_member(user_id)
#         if not member:
#             raise ValueError('Member not found')
#         return member
#
#     def delete_member(self, user_id, chat_id):
#         members = self.get_members_by_chat(chat_id)
#         for member in members:
#             if member.user_id == user_id:
#                 member.kicked = datetime.now()
#                 return self._repository.delete(user_id)
#         return None
#
#     @staticmethod
#     def is_owner(owner, chat):
#         if owner.pk == chat.owner:
#             return True
#         return False
#
#     def is_member(self, user_id, chat_id):
#         members_by_chat = self.get_members_by_chat(chat_id)
#         for member in members_by_chat:
#             if user_id == member.user_id:
#                 return True
#         return False
#
#     def add_member_to_chat(self, member: ChatMember):
#         return self.create_members(member)
#
#
# message_service = MessageService(messages_repo=message_storage)
# chat_service = ChatService(chats_repo=chat_storage, members_repo=chat_member_storage)
# chat_member_service = ChatMemberService(repository=chat_member_storage)