import logging
from urllib.parse import parse_qsl

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import get_user_model

from apps.chat.modules.cache import ChatRoomsCache
from apps.chat.utils import generate_chat_room_name

User = get_user_model()
logger = logging.getLogger(__name__)


class ChatEchoConsumer(JsonWebsocketConsumer):
    """
    Consumer which handle chat websockets events for the echo test user.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None

    def connect(self):
        self.user: User = self.scope["user"]
        if not self.user.is_authenticated:
            return
        self.accept()
        logger.info("Connected websocket for ECHO TEST user")
        self.send_json(
            {
                "type": "chat.information",
                "user": self.user.username,
                "message": "The are now successfully connected to ECHO test user!",
            }
        )

    def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "chat.message":
            # Send the user message
            self.send_json(
                {
                    "type": "chat.message",
                    "user": self.user.username,
                    "message": content.get("message", "Nothing"),
                }
            )
            # Send the echo response
            self.send_json(
                {
                    "type": "chat.message",
                    "user": "echo",
                    "message": f"You said: {content.get('message', 'Nothing')}",
                }
            )
        return super().receive_json(content, **kwargs)

    def disconnect(self, code):
        logger.info("Disconnected websocket for ECHO TEST user")
        return super().disconnect(code)


class ChatConsumer(JsonWebsocketConsumer):
    """
    Consumer which handle chat websocket events.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.chat_user: str = ""
        self.chat_room_name: str = ""

    def connect(self):
        # Check user is authenticated
        self.user: User = self.scope["user"]
        if not self.user.is_authenticated:
            return

        # Get chat user from query params and generate the room name if the same user exists in database
        query_params = dict(parse_qsl(self.scope["query_string"].decode("utf-8")))
        self.chat_user = query_params["chat_user"]
        self.chat_room_name = generate_chat_room_name(
            self.user.username, self.chat_user
        )
        if not self.chat_room_name:
            return

        # Connect websocket
        self.accept()
        logger.info(f"Connected websocket for {self.chat_user} in chat room {self.chat_room_name}")  # fmt: skip

        # * -------- Add user to chat room -------
        ChatRoomsCache.add_user_to_chat_room(self.chat_room_name, self.user)

        # * ----------- CHANNEL LAYERS -----------
        # Create a channel layer group with the chat room name
        async_to_sync(self.channel_layer.group_add)(self.chat_room_name, self.channel_name)  # fmt: skip
        # * Send users connected in the chat room
        self.send_chat_room_users_connected()
        # * Send connection confirmation message to group
        self.send_to_channel_group(
            {
                "type": "chat.information",
                "user": self.user.username,
                "message": f"The user {self.user.username} is now connected!",
            }
        )

    def receive_json(self, content: dict, **kwargs):
        if content["type"] == "chat.message":
            self.send_to_channel_group(
                {
                    "type": content["type"],
                    "user": self.user.username,
                    "message": content.get("message", "Nothing"),
                }
            )
        return super().receive_json(content, **kwargs)

    def disconnect(self, code):
        # * -------- Remove user from chat room -------
        ChatRoomsCache.remove_user_from_chat_room(self.chat_room_name, self.user)
        # * Send users connected in the chat room
        self.send_chat_room_users_connected()
        # Send a notification message to the channel group
        self.send_to_channel_group(
            {
                "type": "chat.information",
                "user": self.user.username,
                "message": f"The user {self.user.username} has left the chat room.",
            }
        )
        # * Remove channel layer
        async_to_sync(self.channel_layer.group_discard)(self.chat_room_name, self.channel_name)  # fmt: skip
        logger.info(f"Disconnected websocket for {self.chat_user} in chat room {self.chat_room_name}")  # fmt: skip
        return super().disconnect(code)

    # * FUNCTIONS
    def send_to_channel_group(self, obj: dict):
        async_to_sync(self.channel_layer.group_send)(self.chat_room_name, obj)

    def send_chat_room_users_connected(self):
        self.send_to_channel_group(
            {
                "type": "chat.room.users",
                "message": ChatRoomsCache.get_chat_room_usernames_as_list(self.chat_room_name),  # fmt: skip
            }
        )

    # * HANDLERS
    def chat_room_users(self, obj: dict):
        # Add users to the message before send to each client
        obj["user"] = self.user.username
        obj["chat_user"] = self.chat_user
        self.send_json(obj)

    def chat_information(self, obj: dict):
        self.send_json(obj)

    def chat_message(self, obj: dict):
        self.send_json(obj)
