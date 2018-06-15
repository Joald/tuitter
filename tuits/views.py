from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.utils.timezone import datetime
# Create your views here.

from .models import Tuit
from .forms import NewTuitForm


def _add_logged_username(request, context):
    if request.user.is_authenticated():
        context['logged_username'] = request.user.username


def index(request):
    latest_tuit_list = Tuit.objects.order_by('-pub_date')[:20]
    user = request.user

    context = {
        'latest_tuit_list': latest_tuit_list,
        'user': user,
        'tuit_number': len(latest_tuit_list)
    }
    return render(request, 'tuits/index.html', context)


def detail(request, tuit_id):
    tuit = get_object_or_404(Tuit, pk=tuit_id)
    return render(request, 'tuits/detail.html', {'tuit': tuit})


def friends(request, username):
    friend_list =
    return render(request, 'tuits/friend_list.html', {'tuit': tuit})


def user_page(request, username):
    user = get_object_or_404(User, username=username)
    tuit_list = Tuit.objects.filter(creator=username).order_by('-pub_date')[:20]

    context = {
        'tuit_list': tuit_list,
        'user': user
    }
    _add_logged_username(request, context)
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
