from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django.db.models import fields
from .models import *
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
            model = User
            fields = ["username","email","password1","password2"]

class LoginFrom(forms.ModelForm):
        class meta :
                model = User
                fields = ['username','password']

# RELEVANCE_CHOICES = (
#     (1, ("Male")),
#     (2, ("Female"))
# )
# class Create_profile(forms.ModelForm):
#         DOB = forms.DateField()
#         gender = forms.ChoiceField(choices=RELEVANCE_CHOICES)
#         class Meta:
#                 model = Profile
#                 fields = ['image','bio','gender','DOB','Age']

class ProfileUpdateForm(forms.ModelForm):
        pass
# 	email = forms.EmailField()
#         class Meta :
#                 model = My_Profile
#                 fields = ['emial' , 'bio' , 'image']
        # class Meta:
        #         model = My_Profile
        #         fields = ['email','bio','image']
        # class Meta :
        #         model = My_Profile 
        #         fields = [ 'email','bio', 'image']