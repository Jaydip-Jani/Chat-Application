from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.forms import UserRegistrationForm
from .models import *
from django.db.models import Q


def index(request, group_name=None):
    group = Group.objects.filter(name=group_name).first()
    chats = ''
    if group:
        chats = Chat.objects.filter(group=group)
    else:
        if group_name != 'favicon.ico':
            group = Group(name=group_name)
            group.save()
    return render(request, 'chat/index.html', {'group_name': group_name, 'chats': chats})


@login_required
def home(request):
    User = get_user_model()
    users = User.objects.all()
    chats = {}
    if request.method == 'GET' and 'u' in request.GET:
        # chats = chatMessages.objects.filter(Q(user_from=request.user.id & user_to=request.GET['u']) | Q(user_from=request.GET['u'] & user_to=request.user.id))
        chats = chatMessages.objects.filter(
            Q(user_from=request.user.id, user_to=request.GET['u']) | Q(user_from=request.GET['u'],
                                                                       user_to=request.user.id))
        chats = chats.order_by('date_created')
    context = {
        "page": "home",
        "users": users,
        "chats": chats,
        "chat_id": int(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    }
    print(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    return render(request, "chat/home.html", context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created!')
            return redirect('chat-login')
        context = {
            "page": "register",
            "form": form
        }
    else:
        context = {
            "page": "register",
            "form": UserRegistrationForm()
        }
    return render(request, "chat/register.html", context)


@login_required
def profile(request):
    context = {
        "page": "profile",
    }
    return render(request, "chat/profile.html", context)
