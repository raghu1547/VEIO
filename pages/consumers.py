import asyncio
import time
import json
from .views import expirein
from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
# from vehicles.models import Flow, Regveh, Gesveh
# from .views import security, securityOfficer
from datetime import datetime


class PageConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Connected", event)
        chat_room = "krishna"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            "type": "websocket.accept",
        })
        # print(self.channel_name, self.chat_room)

        # # print(self)
        # # self.in_data = []
        # # while True:
        # #     self.out_data = await getFlow()|
        # #     # print(self.in_data == self.out_data)
        # #     if self.in_data != self.out_data:
        # #         await asyncio.sleep(1)
        # #         await self.send({
        # #             "type": "websocket.send",
        # #             "text": json.dumps(self.out_data, default=myconverter)
        # #         })
        # #         self.in_data = self.out_data
        # #         # print(self.in_data)
        # #     await asyncio.sleep(10)

    async def websocket_receive(self, event):
        print("receive", event)
        # self.in_data = []
        # print("hello ladies")
        # print(self.in_data == self.out_data)
        # if self.in_data != self.out_data:
        # await asyncio.sleep(1)
        # print("jai balayya")
        # await self.send({
        #     "type": "websocket.send",
        #     "text": self.out_data
        # })
        # self.in_data = self.out_data
        # print(self.in_data)
        # await asyncio.sleep(10)
        # self.out_data
        await self.channel_layer.group_send(
            "krishna",
            {
                "type": "chat_message",
                "text": "outdata"
            }
        )

    async def chat_message(self, event):
        # print(self)
        print('message', event)
        outdata = await getFlow()
        await self.send({
            "type": "websocket.send",
            "text": json.dumps(outdata, default=myconverter)
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)
        # await self.close()


def myconverter(o):
    if isinstance(o, datetime):
        return o.strftime("%d/%m/%y , %H:%M")


@ database_sync_to_async
def getFlow():
    out_data = []
    out_data = list(expirein())
    return out_data
