from rest_framework import serializers
from .models import Conversation, Message
from users.serializers import UserSerializer 

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # ✅ nested full user objects
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = '__all__'

    def get_last_message(self, obj):
        message = obj.messages.order_by('-timestamp').first()
        return MessageSerializer(message).data if message else None