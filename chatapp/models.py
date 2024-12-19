from django.db import models
from django.contrib.auth.models import User
# db to maintane chat groups
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128,unique=True)
    def __str__(self):
        return self.group_name

# db to maintain  aagroup messages
class GroupMassages(models.Model):
    group=models.ForeignKey(ChatGroup,related_name='chat_messages',on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
       return f'{self.author.username} : {self.body}'
    class Meta:
        ordering=['-created']