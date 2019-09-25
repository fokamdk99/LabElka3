'''
przeniesione do home.routing

from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:conversation_name>/', consumers.ChatConsumer),
]'''