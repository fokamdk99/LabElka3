from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
#from .models import Konwersacja
import string
import random
from .models import Message, Conversation
from django.contrib.auth import get_user_model
User = get_user_model()
from .views import get_messages


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['conversation_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
           self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    #funkcje------------------------------------

    def server_receive_message(self, data):
        '''N = 20
        res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N)) 
        konfa = Konwersacja(name=res)
        konfa.users.add(request.user)
        konfa.save()
        print(f"nazwa konwersacji: {konfa.name}")'''

        print(f"wchodze do server_receive_message")
        message = data['message']
        text_data = json.dumps({
            'command':'js_receive_data',
            'message':message
        })
        self.send(text_data)

    def server_send_response(self,data):
        print(f"wchodze do server_send_response")
        message = data['message']
        auth = data['author']
        nazwa_konwersacji = data['konwersacja']
        author = User.objects.get(username=auth)
        konwersacja = Conversation.objects.get(name=nazwa_konwersacji)
        konwersacja.save()
        wiadomosc = Message(author=author, content=message, belongs_to_conversation=konwersacja)
        wiadomosc.save()
        '''text_data = json.dumps({
            'command':'js_receive_message',
            'message':message
        })
        self.send(text_data)'''
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':self.message_to_json(wiadomosc),                
            }
        )

    def fetch_messages(self, data):
        print(f"wchodze do fetch_messages")
        conv = data['conversation']
        if(conv == ''):
            username = data['username']
            friend = data['friend']
            messages = get_messages(username, friend)[1]
        else:
            print(f'conversation name: {conv}')
            conversation = Conversation.objects.get(name=conv)
            messages = conversation.messages.order_by('-timestamp').all()
        text_data = json.dumps({
            'command': 'show_fetched_messages',
            'messages': self.messages_to_json(messages)

        })
        self.send(text_data)


    commands = {
        'server_receive_message':server_receive_message,
        'server_send_response': server_send_response,
        'fetch_messages':fetch_messages
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
        )'''

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'command':'js_receive_message',
            'message': message
        }))

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author':message.author.username,
            'content':message.content,
            #'timestamp':str(message.timestamp)
            'timestamp':message.timestamp.strftime('%Y-%m-%d %H:%M')
        }