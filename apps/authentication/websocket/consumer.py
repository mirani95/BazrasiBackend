from channels.generic.websocket import AsyncWebsocketConsumer
from apps.product.models import SaleUnit
from asgiref.sync import sync_to_async
import json


@sync_to_async
def get_unit(unit_id=None):
    unit = SaleUnit.objects.get(id=int(unit_id))
    return unit


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected!"}))

    async def disconnect(self, close_code):
        print("WebSocket disconnected!")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        unit = await get_unit(int(message))
        print("Received:", message)

        await self.send(text_data=json.dumps({
            "message": unit.unit
        }))


class SendFromServerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'mojtaba_group'  # noqa
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected!"}))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        msg = data.get("message", "")

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": msg
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            "message": message
        }))

