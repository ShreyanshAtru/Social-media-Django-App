from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
# Create your models here

class My_Profile(models.Model):
    user   = models.OneToOneField(User,on_delete=models.CASCADE)
    image  = models.ImageField(default='profile_pic/default.png' , upload_to = 'profile_pic' )
    bio    = models.TextField(max_length=200,help_text='short info about u')
    gender = models.CharField(max_length=20)
    DOB    = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=30 , blank=True , null=True)
    birth_date = models.DateField(null=True , blank = True)
   

 

    def __str__(self):
        return(self.user.username)

# class FriendRequest(models.Model):
#     to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
#     from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self) :
#         return  "From {}, to {}".format(self.from_user.username, self.to_user.username)