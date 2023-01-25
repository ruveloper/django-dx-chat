from channels.generic.websocket import JsonWebsocketConsumer


class ChatConsumer(JsonWebsocketConsumer):
    """
    Consumer which handle online status and the main chat websocket events.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_name = None

    def connect(self):
        print("Connected!")
        self.chat_name = "home"
        self.accept()
        self.send_json(
            {
                "type": "welcome_message",
                "message": "Hey there! You've successfully connected!",
            }
        )

    def receive_json(self, content, **kwargs):
        print(content)
        return super().receive_json(content, **kwargs)

    def disconnect(self, code):
        print("Disconnected!")
        return super().disconnect(code)
