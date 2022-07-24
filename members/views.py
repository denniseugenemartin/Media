from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from .forms import CustomUserCreationForm
import pdb
from django.forms.models import model_to_dict

def about(request):
    return render(request, 'members/about.html')

def watchlist(request):
    if request.user.is_active:
        user = request.user
        data = user.profile.watchlist
        #pdb.set_trace()

    return render(request, 'members/watchlist.html', data)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return render(request, 'movies/index.html')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Username/Password invalid')
            return render(request, 'members/login.html')
    else:
        return render(request, 'members/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return render(request, 'movies/index.html')


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful!")
            return render(request, 'movies/index.html')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form
    }
    return render(request, 'members/register.html', context)