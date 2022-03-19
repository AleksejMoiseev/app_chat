import pytest


Base_URL = 'http://127.0.0.1:8080/'


class TestUserService:

    def test_register_user(self, user, user_service):
        actor = user_service.register(user)
        assert actor.pk == 0

    def test_get_user(self, user1, user_service):
        actor = user_service.get_user(pk=user1.pk)
        assert actor.username == user1.username
        assert actor.email == user1.email
        assert actor.password == user1.password
        assert actor.access_token == user1.access_token

    def test_get_users(self, users, user_service):
        actors = user_service.get_users()
        assert len(actors) == len(users)

    @pytest.mark.parametrize('limit, offset', [(1, 3), (3, 1)])
    def test_get_users_by_limit(self, limit, offset, user_service, user_repo):
        user_service.get_users(limit=limit, offset=offset)
        user_repo.get_list.assert_called_with(limit=limit, offset=offset)


class TestChatService:

    def test_register_chat(self, chat_service, chat):
        ch = chat_service.register_chat(chat)
        assert ch.pk == 0

    def test_create_chat(self, chat_service, chat, chat0):
        assert chat_service.create_chat(chat) == chat0

    def test_delete_chat(self, chat0, chat_service):
        assert chat_service.delete_chat(chat0.pk) == chat0

    def test_get_chat(self, chat0, chat_service):
        assert chat_service.get_chat(chat0.pk) == chat0

    def test_get_chats(self, chats, chat_service):
        ch = chat_service.get_chats()
        assert len(ch) == len(chats)


class TestMessageService:

    def test_send_message(self, message_service, message, message0):
        m = message_service.send_message(message)
        assert m.pk == 0

    def test_get_messages(self, message_service, messages):
        ms = message_service.get_messages()
        assert len(ms) == len(messages)

    @pytest.mark.parametrize('chat_id, expected', [(0, 10), (1, 0)])
    def test_get_messages_by_chat_id(self, chat_id, expected, message_service):
        assert len(message_service.get_messages_by_chat_id(
            chat_id=chat_id,
            user_id=None,
            limit=None,
            offset=None,)) == expected

    @pytest.mark.parametrize('limit, offset', [(1, 3), (3, 1)])
    def test_get_messages_by_limit(self, limit, offset, message_service, message_repo):
        message_service.get_messages(limit=limit, offset=offset)
        message_repo.get_list.assert_called_with(limit=limit, offset=offset)


class TestChatMemberService:

    def test_get_members(self, chat_member_service, chat_members):
        cms = chat_member_service.get_members()
        assert len(cms) == len(chat_members)

    def test_create_members(self, chat_member_service, chat_member):
        cm = chat_member_service.create_members(chat_member)
        assert cm.pk == 0

    @pytest.mark.parametrize('chat_id, expected', [(0, 8), (1, 0)])
    def test_get_members_by_chat(self, chat_id, expected, chat_member_service):
        assert len(chat_member_service.get_members_by_chat(chat_id=chat_id)) == expected

    def test_get_member(self, chat_member_service, chat_member0):
        assert chat_member_service.get_member(chat_member0.pk) == chat_member0

    def test_is_owner(self, owner, chat, chat_member_service):
        assert chat_member_service.is_owner(owner, chat) is True

    def test_is_member(self, user1, chat0, chat_member_service):
        assert chat_member_service.is_owner(user1, chat0) is True

    def test_add_member_to_chat(self, chat_member_service, chat_member, chat_member0):
        assert chat_member_service.add_member_to_chat(chat_member) == chat_member0
