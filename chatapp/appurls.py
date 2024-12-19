# this is apps url
from django.contrib import admin
from django.urls import path
from django.urls import include
from chatapp import views
from .views import *
urlpatterns = [
    
    path("",views.chat_view,name="home"),
    path("home",views.chat_view,name="home")

]
