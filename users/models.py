from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static# used to display a default avtar image
# profile baised db

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    display_name = models.CharField(max_length=128, unique=True)
    info = models.TextField(max_length=120, unique=True)

    def __str__(self):
        return str(self.user)

    @property
    def name(self):
        if self.display_name:
            name=self.display_name
        else:
            name=self.user.username
        return name
    
    @property
    def avatar(self):
        try:
          avatar= self.profile_picture.url
        except:
          avatar= static('account-avatar-profile-user-14-svgrepo-com (1).svg')
        return avatar

