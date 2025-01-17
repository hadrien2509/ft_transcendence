from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MyGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the user to a specific group
        await self.channel_layer.group_add("game_room", self.channel_name)
        self.username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the group
        await self.channel_layer.group_discard("game_room", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            "game_room",
            {
                'type': 'chat_message',
                'message': message,
                'username': self.username
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'username': event['username'],  # Send the username along with the message
            'message': event['message']
        }))
