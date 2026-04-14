from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # ws://localhost:8000/ws/chat/123/
    # 123 = conversation id
    re_path(
        r"ws/chat/(?P<conversation_id>\d+)/$",
        consumers.ChatConsumer.as_asgi()
    ),
]