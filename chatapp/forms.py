from django.forms import ModelForm
from django import forms
from .models import *

class ChatmessagesCreateForm(ModelForm):
    class Meta:
        model=GroupMessages
        fields=['body']
        widgets={
            'body':forms.TextInput(attrs={'placeholder':'Add message ...','class':'p-4 h-[60px] text-black outline-none border-none rounded-tl-[20px] rounded-bl-[20px] rounded-tr-[0px] rounded-br-[0px] mt-8 w-[65em] ','maxlength':'300','autofocus':True}),
                                          
        }
 
class NewGroupForm(ModelForm):
    class Meta:
        model=ChatGroup
        fields=['groupchat_name']
        widgets={
            'groupchat_name':forms.TextInput(attrs={
            'placeholder':'Add name ...',
            'class':'p-4 text-black',
            'maxlength':'300',
            'autofocus':True,
            }),
                
            
        }