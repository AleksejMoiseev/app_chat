import pytest


class TestUserService:

    def test_register_user(self, user, user_service):
        actor = user_service.register(user)
        assert actor.id == 0

    def test_get_user(self, user1, user_service):
        actor = user_service.get_user(pk=user1.id)
        assert actor.username == user1.username
        assert actor.email == user1.email
        assert actor.password == user1.password

    def test_get_users(self, users, user_service):
        actors = user_service.get_users()
        assert len(actors) == len(users)

    @pytest.mark.parametrize('limit, offset', [(1, 3), (3, 1)])
    def test_get_users_by_limit(self, limit, offset, user_service, user_repo):
        user_service.get_users(limit=limit, offset=offset)
        user_repo.get_list.assert_called_with(limit=limit, offset=offset)
