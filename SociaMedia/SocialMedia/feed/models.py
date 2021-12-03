from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.conf import settings 
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from login.models import My_Profile
# Create your models here.

class Post(models.Model):
    body       = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author     = models.ForeignKey(User , on_delete=CASCADE)

class Comment(models.Model):
    comment    = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author     = models.ForeignKey(User , on_delete=models.CASCADE)
    post       = models.ForeignKey('Post',on_delete=models.CASCADE)

# class UserProfile(models.Model):
#     user = models.OneToOneField(User , primary_key = True , verbose_name ='user', related_name='profile1' , on_delete= models.CASCADE)
#     name = models.CharField(max_length=30 , blank=True , null=True)
#     bio  = models.TextField(max_length=300,blank=True)
#     birth_date = models.DateField(null=True , blank = True)
#     location = models.CharField(max_length=100,blank=True)
#     picture  = models.ImageField(upload_to = 'profile_pic' , default='profile_pic/default.png')

# class FriendList(models.Model):
#     user 	= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
#     friends = models.ManyToManyField(User, blank = True , related_name = 'friends')



#     def __str__(self):
#         return self.user.username
    
#     def add_friends(self,account ):

#         """
#         Add a new friend
#         """
#         if not account in self.friends.all():
#             self.friends.add(account)
#             self.save()
    
#     def remove_friend(self,account):
#         """
#         Removing a friend 
#         """
#         if account in self.friends.all():
#             self.freinds.remove(account)
# @receiver(post_save , sender=User)
# def crerate_user_profile(sender , instance , created , **kwargs):
#     if created :
#         UserProfile.objects.create(user=instance)
# @receiver(post_save , sender=User)
# def save_user_profile(sender ,instance, **kwargs):
#     instance.profile.save()

