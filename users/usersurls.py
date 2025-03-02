# this is apps url
from django.contrib import admin
from django.urls import path
from django.urls import include
from users.views import *
from . import views
urlpatterns = [
    
    # path('',profile_view,name="profile"),
    path('',profile_view, name="profile"),
    path('profile-edit',profile_edit_view,name="profile-edit"),
    path('profile-onboardig/',profile_edit_view,name="profile-onboarding"),
    path('settings/',profile_settings_view,name="profile-settings"),
    path('emailchange/',profile_emailchange,name="profile-emailchange"),
    path('emailverify/',profile_emailverify,name="profile-emailverify"),
    path('delete/',profile_delete_view,name="profile-delete")
    
]
