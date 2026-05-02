import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from .models import Conversation, Message
from .serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"
        self.connected = False

        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        is_participant = await self.check_participant()
        if not is_participant:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()
        self.connected = True

        online_user_ids = await self.mark_user_online()

        for user_id in online_user_ids:
            if user_id != self.user.id:
                await self.send_presence_update(user_id, "online")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "presence_update",
                "user_id": self.user.id,
                "status": "online",
            },
        )

        print(f"{self.user.username} connected to conversation {self.conversation_id}")

    async def disconnect(self, close_code):
        if not getattr(self, "connected", False):
            return

        is_offline = await self.mark_user_offline()

        if is_offline:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "presence_update",
                    "user_id": self.user.id,
                    "status": "offline",
                },
            )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        print(f"{self.user.username} disconnected from conversation {self.conversation_id}")

    async def presence_update(self, event):
        await self.send_presence_update(event["user_id"], event["status"])

    async def send_presence_update(self, user_id, status):
        await self.send(text_data=json.dumps({
            "type": "presence",
            "user_id": user_id,
            "status": status,
        }))

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            content = data.get("content", "").strip()

            if not content:
                return

            message = await self.save_message(content)
            message_data = await self.serialize_message(message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message_data,
                },
            )

        except json.JSONDecodeError:
            pass

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "message",
            "message": event["message"],
        }))

    @database_sync_to_async
    def check_participant(self):
        return Conversation.objects.filter(
            id=self.conversation_id,
            participants=self.user,
        ).exists()

    @database_sync_to_async
    def save_message(self, content):
        conversation = Conversation.objects.get(id=self.conversation_id)
        return Message.objects.create(
            conversation=conversation,
            sender=self.user,
            content=content,
        )

    @database_sync_to_async
    def serialize_message(self, message):
        return MessageSerializer(message).data

    @sync_to_async
    def mark_user_online(self):
        presence = cache.get(self.presence_cache_key, {})
        user_id = str(self.user.id)
        presence[user_id] = presence.get(user_id, 0) + 1
        cache.set(self.presence_cache_key, presence, timeout=None)
        return [int(id) for id, count in presence.items() if count > 0]

    @sync_to_async
    def mark_user_offline(self):
        presence = cache.get(self.presence_cache_key, {})
        user_id = str(self.user.id)

        if user_id not in presence:
            return True

        presence[user_id] -= 1
        if presence[user_id] <= 0:
            del presence[user_id]
            is_offline = True
        else:
            is_offline = False

        cache.set(self.presence_cache_key, presence, timeout=None)
        return is_offline

    @property
    def presence_cache_key(self):
        return f"presence:conversation:{self.conversation_id}"
