from django.contrib import admin
from .models import My_Profile
from feed.models import Comment
# from .models import FriendRequest
# from .models import User
# Register your models here.
admin.site.register(My_Profile)
# admin.site.register(FriendRequest)
admin.site.register(Comment)

