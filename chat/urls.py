from django.urls import path

from . import views

urlpatterns = [
    path('<slug:friend_username>', views.chat_index, name='conversation')
]