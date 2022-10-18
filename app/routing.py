from . import consumers
from django.urls import path

websocket_urlpatterns = [
    path('ws/wsc/<str:group_name>/', consumers.MyWebsocketConsumer.as_asgi())
]
