from django.contrib.auth.models import User
from .models import Profile


# post_save is a signal that is sent after a model object is saved
from django.db.models.signals import post_save, post_delete
# receiver is a decorator that receives the signal and performs some task
from django.dispatch import receiver


# SEND MAIL

from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # check if is a new instance
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username.lower(),
            email=user.email,
            name=user.first_name,

        )

def update_profile(sender, instance, created, **kwargs):
    pass

@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    user = instance.user
    user.delete()


