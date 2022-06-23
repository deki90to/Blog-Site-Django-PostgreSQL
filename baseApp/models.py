from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.db.models.signals import post_save
from django_resized import ResizedImageField
from birthday import BirthdayField, BirthdayManager

# from django.db.models.signals import post_save
# from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    profile_image = ResizedImageField(size=[1280, 720], quality=100, null=True, blank=True, upload_to='profil_images/')
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    birthday = BirthdayField(blank=True, null=True)
    objects = BirthdayManager()

    def __str__(self):
        return f'{self.first_name, self.last_name, self.email, self.phone}'



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.TextField()
    image = ResizedImageField(size=[1280, 720], quality=100, null=True, blank=True, upload_to='images/')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    
    def __str__(self):
        return f'{self.post}'
    
    class Meta:
        ordering = ['-created']


# def create(sender, instance, created, **kwargs):
#     if created:
#         Post.objects.create(user=instance)
#         print('CREATED')

# post_save.connect(create, sender=User)


        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user}: {self.comment}'
    
    class Meta:
        ordering = ['-created']
        
        
