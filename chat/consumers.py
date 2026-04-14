# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Conversation, Message
from .serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user            = self.scope["user"]
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        is_participant = await self.check_participant()
        if not is_participant:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # ✅ Broadcast to all users in room that this user is online
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":    "presence_update",
                "user_id": self.user.id,
                "status":  "online",
            }
        )

        print(f"✅ {self.user.username} connected to conversation {self.conversation_id}")
        
        
    async def disconnect(self, close_code):
    # ✅ Broadcast that user went offline
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":    "presence_update",
                "user_id": self.user.id,
                "status":  "offline",
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"❌ {self.user.username} disconnected from conversation {self.conversation_id}")



    async def presence_update(self, event):
        await self.send(text_data=json.dumps({
            "type":    "presence",
            "user_id": event["user_id"],
            "status":  event["status"],
        }))

        
    async def receive(self, text_data):
        # Receive message from WebSocket
        try:
            data    = json.loads(text_data)
            content = data.get("content", "").strip()

            if not content:
                return

            # Save message to database
            message = await self.save_message(content)

            # Serialize message
            message_data = await self.serialize_message(message)

            # Broadcast to everyone in the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type":    "chat_message",   # calls chat_message() method below
                    "message": message_data,
                }
            )

        except json.JSONDecodeError:
            pass


    # ── Called when a message is broadcast to the group ─────────────────────
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket client
        await self.send(text_data=json.dumps({
            "type":    "message",
            "message": message,
        }))


    # ── Database operations (sync → async) ──────────────────────────────────
    @database_sync_to_async
    def check_participant(self):
        return Conversation.objects.filter(
            id=self.conversation_id,
            participants=self.user
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