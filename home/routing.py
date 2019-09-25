from django.urls import path

from .consumers import HomeConsumer
from chat.consumers import ChatConsumer


websocket_urlpatterns = [
    path('ws/home/homepage/', HomeConsumer),
    path('ws/chat/<str:conversation_name>/', ChatConsumer),

]