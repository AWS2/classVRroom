import json
from channels.generic.websocket import AsyncWebsocketConsumer


class EntregaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'entrega'

        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        id = text_data_json["id"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "entrega_editada",
                "id": id
            }
        )
    
    async def entrega_editada(self, event):
        id = event["id"]

        await self.send(text_data=json.dumps({
            'id': id,
        }))

    pass