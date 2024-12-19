from django.shortcuts import render,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
# Create your views here.
@login_required
def chat_view(request):
    chat_group=get_object_or_404(ChatGroup,group_name="public_chat")
    chat_messages=chat_group.chat_messages.all()[:30]
    return render (request,'base.html',{'chat_messagees': chat_messages})
