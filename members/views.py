from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from movies.views import lookup_obj
from .forms import CustomUserCreationForm
from django.forms.models import model_to_dict


def about(request):
    return render(request, 'members/about.html')

def watchlist(request):
    if request.user.is_active:
        user = request.user
        data = user.profile.watchlist
    return render(request, 'members/watchlist.html', data)

# takes post result and authenticates it. If successful login and return to index with success message. If unsuccessful
# reload login page with error message.
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

# Logout user and return to index with success message.
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return render(request, 'movies/index.html')

# If view gets POST data then validate it and present success message. Otherwise, display form on registration page.
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

# Remove a media object from user's watchlist.
def remove_media(request, number):

    # if the user is logged in, get their watchlist and store it in a variable
    if request.user.is_active:
        user = request.user
        response = user.profile.watchlist.get('data')

        # Regenerate list with items that do not match id field of requested media object.
        response[:] = [x for x in response if x['id'] != number]
        user.save()
        messages.success(request, "Media deleted from watchlist.")
        return redirect('watchlist')

    # if the user is not logged in, give an error and send to login page.
    else:
        messages.error(request, "You must login to edit a watchlist.")
        return render(request, 'members/login.html')

# save movie to user's watchlist. it will create a movie object using the create_movie_obj function. Then it will check
# if the user is logged in. If they are, then it will get their watchlist data and append the id number of the movie to
# that list or create a new watchlist with this number as the first entry. User will then be sent back to index page
# with a success message. If user is not logged in they will be sent to login page with an error message instead.

def save_media(request, number):

    # find or create the object using the id number provided to function
    instance = lookup_obj(number)

    # convert media object to a dict object in order to serialize
    media = model_to_dict(instance)

    # if the user is logged in, get their watchlist and store it in a variable
    if request.user.is_active:
        user = request.user
        response = user.profile.watchlist.get('data')

        # check to see if user already has a non empty watchlist
        if user.profile.watchlist:

            # if this item has the same id (pk) as an item already in the user's watchlist, return an error message and
            # don't update anything.
            for item in response:
                if item['id'] == number:
                    messages.error(request, "Item already exists in your watchlist.")
                    return render(request, "movies/media_detail.html", {'data': instance})
            response.append(media)
            user.profile.watchlist = {'data': response}

        # if the user does not have a watchlist, add this object to a new list and update the watchlist with this info.
        else:
            datalist = [media]
            user.profile.watchlist.update({'data': datalist})

        # if the logic makes it to the save step then the user was logged in and the object did not already exist in
        # their watchlist. Save, reload page with success message.
        user.save()
        messages.success(request, "Watchlist updated.")
        return render(request, "movies/media_detail.html", {'data': instance})

    # if there is no logged in user, present an error message and send to login page
    else:
        messages.error(request, "You must login to save to a watchlist.")
        return render(request, 'members/login.html')