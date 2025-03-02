# this is similer file like urls.py which only works for the web socket connnections
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json
from .models import *

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user=self.scope['user']# now we cant use request object here we can use 
        #scope dictionary which gives information about loggedin user provided by auth middwaerstack
        self.chatroom_name=self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom=get_object_or_404(ChatGroup,group_name=self.chatroom_name)
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,self.channel_name
        )
        # add and update online users
        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()
            self.accept()
    # removes teh channal from the chat group
    def disconnect(self, clos_code):
        async_to_sync(self.channel_layer.group_discard)(self.chatroom_name,self.channel_name)
        # remove and update online usser
        if self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()
    # this resives the data in text_data parameter converting geson to python object
    def receive(self,text_data):
        text_data_jeson=json.loads(text_data)
        body= text_data_jeson['body']
        message=GroupMessages.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )
       
        event={
           'type':'message_handler',
           'message_id':message.id
        }
        async_to_sync(self.channel_layer.group_send)(self.chatroom_name,event)

    def message_handler(self,event):
        message_id=event['message_id']
        message=GroupMessages.objects.get(id=message_id)
        context={
            'message': message,
            'user': self.user,  
            }
        html=render_to_string("chatapp/partials/chat_messages_p.html",context=context)
        #render_to_string is smiler function live return statement in views 
        self.send(text_data=html)
    def update_online_count(self):
     online_count = self.chatroom.users_online.count() -1
     event = {
        'type': 'online_count_handler',
        'online_count': online_count
     }
     async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)

    
    def online_count_handler(self,event):
        online_count=event['online_count']
        context={
            'online_count':online_count,
            'chat_group':self.chatroom
        }
        html=render_to_string("chatapp/partials/online_count.html",context)
        self.send(text_data=html)


