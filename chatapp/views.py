from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from .forms import ChatmessagesCreateForm
# Create your views here.

@login_required
def chat_view(request):
    chat_group=get_object_or_404(ChatGroup,group_name="public-chat")
    chat_messages=chat_group.chat_messages.all()[:40]
    form=ChatmessagesCreateForm()
    # logic for database save htx post request
    if request.htmx:
       form=ChatmessagesCreateForm(request.POST)
       if form.is_valid():     
          message=form.save(commit=False)
          message.author=request.user
          message.group=chat_group
          message.save()
          context = {'message': message, 'user': request.user}
          return render(request,'chatapp/partials/chat_messages_p.html',context)

    return render (request,'chatapp/chat.html',{'chat_messages': chat_messages,'form': form})
    # return render(request,'chatapp/chat.html')