# Import System Modules
import json

# Import Third-party Python Modules
from channels.generic.websocket import AsyncWebsocketConsumer
from googletrans import Translator


# Import Project Modules

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        lang = data.get('lang', 'en')

        # Translate the message
        translator = Translator()
        translated_message = translator.translate(message, dest=lang).text

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name,
                                            {'type': 'chat_message', 'message': translated_message})

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))
