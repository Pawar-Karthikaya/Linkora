from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        participants = request.data.get('participants')

        if not participants or len(participants) == 0:
            return Response({"error": "participants field is required"}, status=400)

        other_user_id = participants[0]

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Check if conversation already exists between these two users
        conversation = Conversation.objects.filter(
            participants=user
        ).filter(
            participants=other_user
        ).distinct()

        if conversation.exists():
            # Conversation found → return existing one
            serializer = self.get_serializer(conversation.first())
            return Response(serializer.data, status=200)

        # Conversation not found → create a new one
        conversation = Conversation.objects.create()
        conversation.participants.add(user, other_user)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=201)

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).distinct()
    
    @action(detail=False, methods=['get'], url_path='my-conversations')
    def my_conversation(self, request):
        conversation = self.get_queryset()
        serializer = self.get_serializer(conversation, many=True)
        return Response(serializer.data)
    


from rest_framework.exceptions import PermissionDenied

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Message.objects.filter(
            conversation__participants=self.request.user
        ).distinct()

        conversation_id = self.request.query_params.get('conversation_id')

        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)

        return queryset.order_by('timestamp')

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not part of this conversation")

        serializer.save(sender=self.request.user)