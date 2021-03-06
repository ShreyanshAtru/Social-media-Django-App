from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

app_name = 'login'
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.homepage,name="Homepage"),
    path("signup",views.signup,name="signup"),
    # path("make_profile",views.make_profile,name="profile"),
    #path("edit_profile", views.edit_profile,name="edit profile"),
    path("login_request",views.login_request,name="login-request"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('userview',views.userview , name = 'user_view')
]