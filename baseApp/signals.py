from . models import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



@receiver(post_save, sender=User)
def created(sender, instance, created, **kwargs):
    # Post.objects.create(user=instance)
    print('User created ', User)