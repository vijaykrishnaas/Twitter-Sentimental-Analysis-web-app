from .module.utils import getLogFormat
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from .views import searchQuery

import logging
logger = logging.getLogger('sentiment')


class SocketConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        # Called on connection
        # To accept the connection call
        await self.accept()
        await self.channel_layer.group_add("status", self.channel_name)
        logger.info(getLogFormat(text="WebSocket Connected!"))

    async def disconnect(self, close_code):
        # Called when the socket closes
        await self.channel_layer.group_discard("chat", self.channel_name)
        logger.info(getLogFormat(text="WebSocket Disconnected!"))

    async def receive(self, text_data):
        # Called with either text_data or bytes_data for each frame
        await self.send(json.dumps(text_data))

    async def status_update(self, event):
        logger.info(getLogFormat(text="Status Update: " + json.dumps(event["text"])))
        await self.send(json.dumps(event["text"]))
