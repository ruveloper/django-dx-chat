from django.urls import path

from apps.chat.consumers.chat_consumers import ChatConsumer, ChatEchoConsumer
from apps.chat.consumers.state_consumers import StateConsumer

# These patterns handle the urls for websockets and is used by the ASGI application
websocket_urlpatterns = [
    path("state/", StateConsumer.as_asgi()),
    path("chat/", ChatConsumer.as_asgi()),
    path("chat/echo/", ChatEchoConsumer.as_asgi()),
]
