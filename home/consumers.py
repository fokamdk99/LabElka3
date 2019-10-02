from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.contrib.auth import get_user_model
User = get_user_model()
from chat.models import Conversation
from home.models import Post
from labelka.models import Komentarz
from .views import comment_to_json
import string
import random

class HomeConsumer(WebsocketConsumer):
    def connect(self):
        pass
        #self.room_name = self.scope['url_route']['kwargs']['room_name']
        #self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        #async_to_sync(self.channel_layer.group_add)(
         #   self.room_group_name,
          #  self.channel_name
        #)

        self.accept()

    def disconnect(self, close_code):
        pass
        # Leave room group
        #async_to_sync(self.channel_layer.group_discard)(
         #   self.room_group_name,
          #  self.channel_name
        #)

    #funkcje------------------------------------

    '''def add_post(self, data):
    author=data['author']
    title=data['title']
    content=data['content']'''

    def server_receive_message(self, data):
        print(f"wchodze w server_receive")
        message = data['message']
        print(f"wiadomosc: {message}")
        text_data = json.dumps({
            'command':'js_receive_data',
            'message':message
        })
        self.send(text_data)

    def server_add_friend(self, data):
        username = data['username']
        friend_username=data['friend_username']
        print(f"server_add_friend, name:{username}, friend: {friend_username}")
        user=User.objects.get(username=username)
        friend=User.objects.get(username=friend_username)
        user.znajomi.add(friend)

        N = 20
        res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N)) 
        print(f'tworze nowa konwersacje: nazwa to: {res}')
        conversation = Conversation(name=res)
        conversation.save()
        conversation.related_users.add(user, friend)
        self.send(json.dumps({
            'command':'js_add_friend_to_dom',
            'username':friend_username
        }))

    def server_add_comment(self, data):
        content = data['content']
        auth=data['author']
        post_id=data['post_id']
        tworca = User.objects.get(username=auth)
        post = Post.objects.get(id=post_id)
        print(f"wchodze do server_add_comment, content: {content}, autor: {auth}, post_id: {post_id}, post_title: {post.title}")
        comment = Komentarz(author=tworca,content=content,post=post)
        comment.save()
        self.send(json.dumps({
            'command':'js_add_comment',
            'comment':comment_to_json(comment),
            'post_id':post_id
        }))


    commands = {
        'server_receive_message':server_receive_message,
        'server_add_friend':server_add_friend,
        'server_add_comment':server_add_comment
    }

    # Receive message from WebSocket
    def receive(self, text_data):
        print(f"wchodze do receive")
        text_data_json = json.loads(text_data)
        self.commands[text_data_json['command']](self,text_data_json)

        '''message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))'''
