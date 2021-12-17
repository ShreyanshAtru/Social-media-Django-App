from datetime import datetime
from time import timezone

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from login.models import My_Profile, Friendship
from django.contrib.auth.views import PasswordChangeView


# Create your views here.
#
# class PasswordsChangeView(PasswordChangeView):
#     from_class = PasswordChangeForm
#     success_url = reverse_lazy('post-list')


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }
        return render(request, 'feed/post_list.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'post_list': posts,
            'form': form,
        }
        return render(request, 'feed/post_list.html', context)


class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments
        }
        return render(request, 'feed/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        context = {
            'post': post,
            'form': form,
            'comments': comments
        }
        return render(request, 'feed/post_detail.html', context)


class PostEditView(UpdateView):
    model = Post
    fields = ['body']
    template_name = 'feed/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        success_url = reverse_lazy('post-list', kwargs={'pk': pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'feed/post_delete.html'
    success_url = reverse_lazy('post-list')


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = My_Profile.objects.get(id=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')

        all_req = Friendship.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        receiver_lst = []
        sender_lst = []
        for i in all_req:
            receiver_lst.append(i.receiver)
            sender_lst.append(i.sender)

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'receiver_lst': receiver_lst,
            'sender_lst': sender_lst,

        }
        return render(request, 'feed/profile.html', context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = My_Profile
    fields = ['name', 'bio', 'birth_date', 'gender', 'image']
    template_name = 'feed/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        pk = self.kwargs['pk']
        profile = self.get_object()
        return self.request.user == profile.user


def search(request):
    query = request.GET.get('query')
    all_req = Friendship.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    receiver_lst = []
    sender_lst = []
    for i in all_req:
        receiver_lst.append(i.receiver)
        sender_lst.append(i.sender)

    profil = User.objects.filter(username__icontains=query)
    return render(request, 'feed/search.html', {'profil': profil, 'receiver_lst': receiver_lst,
                                                'sender_lst': sender_lst})


def send_friend_request(request, pk):
    # import pdb
    # pdb.set_trace()
    sender = request.user
    receiver = User.objects.get(pk=pk)
    friend_request, created = Friendship.objects.get_or_create(sender=sender, receiver=receiver, status='Sent')
    if created:
        context = My_Profile.objects.all()
        return render(request, 'feed/send_request_feed.html', {'context': context})
    else:
        context = My_Profile.objects.all()
        return render(request, 'account/friends.html', {'context': context})


def are_friends(sender, receiver):
    if sender and receiver in Friendship.objects.filter(status='Sent'):
        return HttpResponse('Already Sent ')
    if Friendship.objects.filter(sender=sender, receiver=receiver).exists():
        return HttpResponse("ready requested friendship from you.")


def accept_friend_request(request, requestid):
    # import pdb
    # pdb.set_trace()
    receiver = request.user
    sender = User.objects.get(pk=requestid)
    friend_request = Friendship.objects.get(sender=sender, receiver=receiver, status="Sent")
    friend_request.status = 'Accepted'
    friend_request.save()
    return render(request, 'feed/friendlist.html')


def friend_list(request):
    # profile = My_Profile.objects.get(pk=userid)
    # user = profile.user
    friends = Friendship.objects.filter(Q(sender=request.user, status='Accepted') | Q(receiver=request.user, status='Accepted'))
    return render(request, 'feed/friendlist.html', {'friends': friends})


def friends_invites(request):
    friends = Friendship.objects.filter(receiver=request.user, status='Sent')
    return render(request, 'feed/friendinvite.html', {'friends': friends})


def change_password(request):
    # import pdb
    # pdb.set_trace()
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('login:logout')
            #return HttpResponse('Password change Successfully')
        else:
            return render(request, 'feed/resetPass.html')
    else:
        form = PasswordChangeForm(user=request.user)
    context = {'form': form}
    return render(request, 'feed/resetPass.html', context)


def unfriend(request, userid):
    import pdb
    pdb.set_trace()
    sender = request.user
    receiver = User.objects.get(id=userid)
    remove_friend = Friendship.objects.get(Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender))
    remove_friend.delete()
    return render(request, 'feed/friendlist.html')
