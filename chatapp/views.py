from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.http import Http404 
from .forms import *
from django.contrib import messages

# Create your views here.
@login_required
def chat_view(request,chatroom_name='public-chat'):
    chat_group=get_object_or_404(ChatGroup,group_name=chatroom_name)
    chat_messages=chat_group.chat_messages.all()[:40]
    form=ChatmessagesCreateForm()
    other_user=None  
    if chat_group.is_private:
       if request.user not in chat_group.members.all():
          raise Http404()
       for member in chat_group.members.all():
           if member!= request.user:
             other_user=member
             break
           
    if  chat_group.groupchat_name:
       if request.user not in chat_group.members.all():
         if request.user.emailaddress_set.filter(verified=True).exists():
           chat_group.members.add(request.user)
         else:
            messages.warning(request,'Plz verify your email to join this chat room')
            return redirect ('profile-settings')
          

             
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
    context={
         'chat_group': chat_group,
         'chat_messages': chat_messages,
         'form': form,
         'other_user': other_user,
         'chatroom_name':chatroom_name

    }
    return render (request,'chatapp/chat.html',context)

from django.shortcuts import get_object_or_404

@login_required
def get_or_create_chatroom(request, username):
    # Prevent users from chatting with themselves
    if request.user.username == username:
        return redirect('home')

    # Fetch the other user or return 404 if they don't exist
    other_user = get_object_or_404(User, username=username)

    # Check if a private chatroom with the other user already exists
    chatroom = (
        request.user.chat_groups.filter(is_private=True, members=other_user)
        .distinct()
        .first()
    )

    # If no chatroom exists, create a new one
    if not chatroom:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(request.user, other_user)

    # Redirect to the chatroom
    return redirect('chatroom', chatroom.group_name)

@login_required
def create_groupchat(request):
    form=NewGroupForm()
    if request.method=='POST':
       form=NewGroupForm(request.POST)
       if form.is_valid():
          new_groupchat=form.save(commit=False)
          new_groupchat.admin=request.user
          new_groupchat.save()
          new_groupchat.members.add(request.user)
          return redirect ('chatroom',new_groupchat.group_name)
    context={
       'form':form
    }
    return render(request,'chatapp/create_groupchat.html',context)