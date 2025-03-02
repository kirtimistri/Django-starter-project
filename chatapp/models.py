from django.db import models
from django.contrib.auth.models import User
import shortuuid

# db to maintane chat groups
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128,unique=True,default=shortuuid.uuid)
    # related_name='online_in_groups'to fetch in  how manay groups the user is online 
    users_online=models.ManyToManyField(User,related_name='online_in_groups',blank=True)
    members=models.ManyToManyField(User, related_name='chat_groups',blank=True)
    is_private=models.BooleanField(default=False)
    groupchat_name=models.CharField(max_length=128,null=True,blank=True)
    admin=models.ForeignKey(User, related_name='groupchats',blank=True,null=True,on_delete=models.SET_NULL)
    def __str__(self):
        return self.group_name

# db to maintain  a group messages
class GroupMessages(models.Model):
    group=models.ForeignKey(ChatGroup,related_name='chat_messages',on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.CharField(max_length=300)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
       return f'{self.author.username} : {self.body}'
    class Meta:
        ordering=['-created']