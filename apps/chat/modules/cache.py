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


class ChatRoomsCache:
    """
    Module to store and manage the information of users connected to each chat room using the cache system.
    """

    User = get_user_model()

    @staticmethod
    def get_chat_room(chat_room_name):
        return cache.get(chat_room_name, [])

    @classmethod
    def add_user_to_chat_room(cls, chat_room_name: str, user: User):
        chat_room: list = cls.get_chat_room(chat_room_name)
        chat_room.append(user)
        cache.set(chat_room_name, chat_room)

    @classmethod
    def remove_user_from_chat_room(cls, chat_room_name: str, user: User):
        chat_room: list = cls.get_chat_room(chat_room_name)
        chat_room.remove(user) if user in chat_room else None
        cache.set(chat_room_name, chat_room)

    @classmethod
    def get_chat_room_usernames_as_list(cls, chat_room_name):
        chat_room: list = cls.get_chat_room(chat_room_name)
        return [user.username for user in chat_room]
