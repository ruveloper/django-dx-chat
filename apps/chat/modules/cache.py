from django.contrib.auth import get_user_model
from django.core.cache import cache


class OnlineUsersCache:
    """
    Module to store and manage the list of online users using the cache system.
    """

    User = get_user_model()

    @staticmethod
    def get_online_users():
        return cache.get("online_users", [])

    @classmethod
    def add_online_user(cls, user: User):
        online_users: list = cls.get_online_users()
        if user not in online_users:
            online_users.append(user)
            cache.set("online_users", online_users)

    @classmethod
    def remove_online_user(cls, user: User):
        online_users: list = cls.get_online_users()
        online_users.remove(user) if user in online_users else None
        cache.set("online_users", online_users)

    @classmethod
    def get_online_users_info_as_dict(cls):
        online_users: list = cls.get_online_users()
        return {user.username: user.avatar_url for user in online_users}
