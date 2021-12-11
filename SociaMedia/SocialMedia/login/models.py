from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here


class My_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pic/default.png', upload_to='profile_pic')
    bio = models.TextField(max_length=200, help_text='short info about u')
    gender = models.CharField(max_length=20)
    DOB = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    friend = models.ManyToManyField(User, blank=True, related_name='friend', null=True)

    def __str__(self):
        return self.user.username


choices_status = (
    ('A', 'Accepted'),
    ('S', 'Sent')
)


class Friendship(models.Model):
    status = models.CharField(max_length=10, choices=choices_status)

    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.sender.username, self.receiver.username)
