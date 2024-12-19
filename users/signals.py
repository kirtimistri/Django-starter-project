from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import User
from .models import UserProfile
from allauth.account.models import EmailAddress

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        # Create UserProfile with default values
        UserProfile.objects.create(
            user=user,
            display_name=instance.username,  # Default display name
            info=f"Default info for {instance.username}",  # Default info
        )
    else:
        # Update or create the user's primary email address in allauth
        email_address = EmailAddress.objects.filter(user=user, primary=True).first()
        if email_address:
            if email_address.email != user.email:
                email_address.email = user.email
                email_address.verified = False
                email_address.save()
        else:
            # Create a new primary email address if it doesn't exist
            EmailAddress.objects.create(  # Corrected to 'objects'
                user=user,
                email=user.email,
                primary=True,
                verified=False
            )
