from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.utils.timezone import datetime

# Create your views here.

from .models import *
from .forms import NewTuitForm


def _get_friendship(friend1, friend2):
    return Friendship.objects.filter(friend1__exact=friend1, friend2__exact=friend2)


def _add_current_user(request, context):
    context['current_user'] = request.user if request.user.is_authenticated() else None


def _get_friend_list(username):
    friendship_list = Friendship.objects.filter(
        Q(friend1__exact=username) |
        Q(friend2__exact=username)
    )
    return [friendship.friend1 if friendship.friend2 == username else friendship.friend2
            for friendship in friendship_list]


def index(request, all_tuits=True):
    if request.user.is_authenticated() and not all_tuits:
        latest_tuit_list = Tuit.objects.filter(
            Q(creator__exact=request.user.username) |
            Q(creator__in=_get_friend_list(request.user.username))
        ).order_by('-pub_date')[:20]
    else:
        latest_tuit_list = Tuit.objects.order_by('-pub_date')[:20]

    context = {
        'latest_tuit_list': latest_tuit_list,
        'tuit_number': len(latest_tuit_list),
        'all_tuits': all_tuits,
    }
    _add_current_user(request, context)
    return render(request, 'tuits/index.html', context)


def friends_tuits(request):
    return index(request, False)


def detail(request, tuit_id):
    tuit = get_object_or_404(Tuit, pk=tuit_id)
    return render(request, 'tuits/detail.html', {'tuit': tuit})


def befriend(request, username):
    if not request.user.is_authenticated():
        return login_required(request)
    friend1 = username if username < request.user.username else request.user.username
    friend2 = request.user.username if username < request.user.username else username
    their_friendship = _get_friendship(friend1, friend2)
    if their_friendship:
        # Protection against people who try to befriend one of their friends
        return user_page(request, username, 'Cannot befriend ' + username)
    Friendship.objects.create(
        friend1=friend1,
        friend2=friend2
    )
    return user_page(request, username, 'Successfully befriended ' + username)


def unfriend(request, username):
    if not request.user.is_authenticated():
        return login_required(request)
    friend1 = username if username < request.user.username else request.user.username
    friend2 = request.user.username if username < request.user.username else username
    their_friendship = _get_friendship(friend1, friend2)
    if not their_friendship:
        # Protection against people try to befriend one of their friends
        return user_page(request, username, 'Cannot unfriend ' + username)
    their_friendship.delete()
    return user_page(request, username, 'Successfully unfriended ' + username)


def friends(request, username):
    context = {
        'friend_list': _get_friend_list(username),
        'target_user': get_object_or_404(User, username=username)
    }
    _add_current_user(request, context)
    return render(request, 'tuits/friend_list.html', context)


def user_page(request, username, extra=''):
    target_user = get_object_or_404(User, username=username)
    tuit_list = Tuit.objects.filter(creator__exact=username).order_by('-pub_date')[:20]

    context = {
        'tuit_list': tuit_list,
        'target_user': target_user,
        'extra': extra
    }
    _add_current_user(request, context)
    context['can_add_friend'] = request.user.is_authenticated and not \
        _get_friendship(min(username, context['current_user'].username),
                        max(username, context['current_user'].username)).exists()
    return render(request, 'tuits/username.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def new_tuit(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login_required')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewTuitForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            text = form.cleaned_data['tuit_text']
            Tuit.objects.create(
                tuit_text=text,
                creator=user.username,
                pub_date=datetime.now()
            )
            return redirect('index')
        else:
            form = NewTuitForm()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewTuitForm()

    return render(request, 'tuits/new_tuit.html', {'form': form})


def login_required(request):
    return render(request, 'registration/login_required.html')
