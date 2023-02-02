import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import get_user_model

from apps.chat.modules.cache import OnlineUsersCache

logger = logging.getLogger(__name__)
User = get_user_model()


class StateConsumer(JsonWebsocketConsumer):
    """
    Consumer which handle online status.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.channel_group_name = "user-state"

    def connect(self):
        self.user: User = self.scope["user"]
        if not self.user.is_authenticated:
            return
        self.accept()
        logger.info(f"Connected websocket state for {self.user.username}")
        # * ------ Add user to online users ------
        OnlineUsersCache.set_online_user(self.user)
        # * ----------- CHANNEL LAYERS -----------
        # Create channel layer with using the chat room name
        async_to_sync(self.channel_layer.group_add)(
            self.channel_group_name, self.channel_name
        )
        # Send online users to channel group in order to be updated by the client
        self.send_online_users()

    def disconnect(self, code):
        # * ---- Remove user from online users ----
        OnlineUsersCache.remove_online_user(self.user)
        # Send online users to channel group in order to be updated by the client
        self.send_online_users()
        logger.info(f"Disconnected websocket state for {self.user.username}")
        return super().disconnect(code)

    # * FUNCTIONS
    def send_online_users(self):
        async_to_sync(self.channel_layer.group_send)(
            self.channel_group_name,
            {
                "type": "state.users.online",
                "message": OnlineUsersCache.get_online_users_info_as_dict(),
            },
        )

    # * HANDLERS
    def state_users_online(self, obj: dict):
        # Add the authenticated user as entry
        obj["user"] = self.user.username
        # Remove self user from users online list before send to client
        obj["message"].pop(self.user.username) if self.user.username in obj["message"] else None  # fmt: skip
        self.send_json(obj)
