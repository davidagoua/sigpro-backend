# suivi/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TDRConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "tdr_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "tdr_updates",
            self.channel_name
        )

    async def tdr_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'tdr_update',
            'data': event['data']
        }))