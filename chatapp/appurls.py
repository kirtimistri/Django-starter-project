# this is apps url
from django.contrib import admin
from django.urls import path
from django.urls import include
from chatapp import views
from .views import *
urlpatterns = [
    
    path('',views.chat_view,name="home"),
    # crreate  private chat  room with this person is check if alredy exist 
    path('chat/<username>',get_or_create_chatroom,name="start-chat"),
    # if it have a chatroom then redirect to the existing chatroom 
    path('chat/room/<chatroom_name>',chat_view,name="chatroom"),
    path('chat/new_groupchat/',create_groupchat,name="new-groupchat")
    
]
