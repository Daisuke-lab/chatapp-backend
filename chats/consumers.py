import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from .views import get_last_30_messages, get_user_contact
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model() 
class ChatConsumer(WebsocketConsumer):
    #(self, data) => self
    def fetch_messages(self, data):
        print('FETCH_MESSAGE in consumer.py')
        #call a model and get last 30 messages and enable it to be edible in html by content
        messages = get_last_30_messages(data['ChatID'])
        print('messages::', messages)
        content = {
            'messages': self.messages_to_json(messages),
            'command': 'messages'
        }
        self.send_message(content)


    def new_message(self, data):
        print('NEW_MESSAGE in consumer.py')
        #I guess data we have gotten so far is just 'message' and 'command' but I assume we will get 'from' later
        #the role of this function is to save new data in data base(create) and put content into send_chat_message
       

        #one chance to change User
        print('DATA in consumer.py::', data)
        #Choices of User are: auth_token, author_message, email, groups, id, is_active, is_staff, is_superuser,
        #  last_login, logentry, name, password, user_permissions
        # author_user = User.objects.filter(name=author)[0]
        # user = Contact.objects.filter(user=author_user)[0]
        user_contact = get_user_contact(data['from'])
        
        # author_user = <UserAccount: kikuchidaisuke.zr@gmail.com> so, foreign key is like that
        message = Message.objects.create(
            contact=user_contact,
            content=data['message']
        )
        completed_message = message.__dict__
        completed_message['name'] = data['from']
        content = {
            'command': 'new_message',

            #this message includes author, message(content) and timestamp
            #the shape would be{'message': [{'author': message.author.username,
            #                               'content': message.content,
            #                               'timestamp': str(message.timestamp)}]}

            #IT USED TO BE 
            #'message': self.message's'_to_json(message)
            # => self.message_to_json(completed_message) => completed_message

            'message': [self.message_to_json(completed_message)]
        }
        current_chat = get_object_or_404(Chat, id=data['ChatID'])
        current_chat.messages.add(message)
        current_chat.save()
        print('current_chat::',current_chat)
        return self.send_chat_messages(content)

    commands = {'fetch_messages':fetch_messages,
    'new_message':new_message}


    #message"s"_to_json
    #all messages you got is dealt with by message_to_json and make a list
    #messages comes from "def new_message"
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            completed_message = message.__dict__
            name = str(message)
            completed_message['name'] = name
            result.append(self.message_to_json(completed_message))
        return result

    #I guess you need to turn it into dict in order to use them in html
    def message_to_json(self, message):
        return {
            # 'author': message.author.username,
            # 'content': message.content,
            # 'timestamp': str(message.timestamp)
            'id':message['id'],
            # message['author] => message.contact.user.name
            'name': message['name'],
            'content': message['content'],
            'timestamp': str(message['timestamp'])
        }




    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
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


    def receive(self, text_data):
        print('RECEIVE in consumer.py')
    # Receive message from WebSocket

    #This method is the first function called after you texted  a message

    #"text_data is the row data coming from html"

    #you load json file and define it as "data"
    #"(self, data)" after self.commands[data['command']] is used in every method here.
    #thanks to this, you can use "data" as input in every single methods


        data = json.loads(text_data)
        #data[command] is fetch_messages or new_messages
        #(self, data) => self)
        if data['command'] == 'new_message':
            self.commands[data['command']](self, data)
        else:
            self.commands[data['command']](self, data)
            

    def send_chat_messages(self, message):
        # Send message to room group
        print('MESSAGE in send_chat_message')
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    def send_message(self, message):
        self.send(text_data=json.dumps(message))
    #it process into def receive
    # Receive message from room group


    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))