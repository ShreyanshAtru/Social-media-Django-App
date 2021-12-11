from django.urls import path
from . import views
from django.urls.resolvers import URLPattern
from .views import PostListView, PostDetailView, PostEditView, PostDeleteView, ProfileEditView, ProfileView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post-delete'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile-edit'),
    path('search', views.search, name='user-search'),
    path('send_friend_request/<int:pk>/', views.send_friend_request,name="send_friend_request"),
    path('accept_friend_request/<int:requestid>/', views.accept_friend_request,name="accept_friend_request"),
]

if settings.DEBUG:
    urlpatterns == static(settings.MEDIA_URL, documents_root=settings.MEDIA_ROOT)
