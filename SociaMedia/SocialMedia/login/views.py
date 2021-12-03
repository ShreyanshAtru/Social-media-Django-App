from django.http.response import HttpResponse
from django.shortcuts import render ,redirect ,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login ,authenticate , logout
from .forms import  SignUpForm , ProfileUpdateForm
from .forms import SignUpForm 
from django.contrib.auth.decorators import login_required
from .models import My_Profile

def homepage(request):
    # form = Create_profile(request.POST)
    return render(request , 'account/hompage.html' )



# User Registeraation
def signup(request):

    if request.method =='POST':
        form=SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            new_profile = My_Profile(user=user)
            new_profile.save()
            messages.success(request,'User has been registered.')
            return HttpResponseRedirect('login_request')
    else :
        form = SignUpForm() 
    return render(request,'account/register.html' , {'form':form} )



# def logout_view(request):
#     logout(request)
#     return render(request , 'account/homepage.html')




def login_request(request):
    #pdb.set_trace()
    if request.method == "POST" :
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # username = form.cleaned_data.get('username')
                # user = User.objects.get(username=username)
                # feed_profile = My_Profile(user=user)
                # feed_profile.save()
                
                current_user = request.user
                print(current_user.id)
                return render(request , 'account/new.html',{'user' : current_user})
               
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "account/login.html", {"form":form})

def logout(request):
    logout(request)
    return render(request,template_name="account/logout.html")


def userview(request):
    # form = Create_profile(request.POST)
    # template_name = 'account/profile.html'
    # return render(request ,template_name , {'form':form})
    context = My_Profile(request.user)  
    context_list = My_Profile.objects.all()
    context_dict = {'list':context_list}
    return render(request,'account/profile.html' , context_dict)



# @login_required
# def make_profile(request):
#     import pdb
#     pdb.set_trace()
#     current_user = request.user
#     print(current_user , current_user.id)
#     if request.method == 'POST':
#         form = Create_profile(request.POST , request.FILES)
#         print(form)
#         if form.is_valid():
#             form.save()
#             a = messages.success(request,'User has been registered.')
#             return redirect(a)
#         else :
#             return messages.error(request,"Invalid username or password.")
#     else :
#         form = Create_profile()


#     return render(request , 'account/update_profile.html' , {'form':form , 'user':current_user})
@login_required
def update_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid() :
            form.save()
