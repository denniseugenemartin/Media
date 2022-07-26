from django.shortcuts import render
import requests
from .models import Media
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pdb
from django.forms.models import model_to_dict
from datetime import date, time, datetime, timedelta


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
                    return render(request, "movies/media_detail.html", {'data':instance})
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
        return render(request, "movies/media_detail.html", {'data':instance})

    # if there is no logged in user, present an error message and send to login page
    else:
        messages.error(request, "You must login to save to a watchlist.")
        return render(request, 'members/login.html')

# try and find the movie object in the database using the id number as key. If object already exists simply return
# the object without making any API calls. If object does not exist, create and fill fields
# with data from API calls. Will also update data if last update was greater than 7 days ago.

def lookup_obj(number):

    # try and get an object using id as key, if it does not exist call create_media_obj function instead.
    try:
        media = Media.objects.get(id = number)
    except Media.DoesNotExist:
        media = create_media_obj(number)

    # datelimit variable will contain a date from 7 days previous to today's date. Parse the date_updated attribute
    # of the media object and compare. if time_updated occurred before the datelimit call create_media_obj to refresh
    # all data associated with object, otherwise return object.
    datelimit = datetime.today() - timedelta(days = 7)
    time_updated = datetime.strptime(media.date_updated, "%Y-%m-%d")
    if time_updated < datelimit:
        create_media_obj(number)
    return media


# Creates a Django model for the media object in the database.
def create_media_obj(number):

    # Make first API call. This is where basic movie info will come from. Parse data using .json() and update data
    # if object already exists in database. Otherwise, create the object with appropriate fields from API.
    api_key = "k_5a9rr4on"
    url = f"https://imdb-api.com/en/API/Title/{api_key}/{number}"
    response = requests.get(url)
    data = response.json()
    media, created = Media.objects.update_or_create(
        id=number,
        title=data['title'],
        year=data['year'],
        image=data['image'],
        imdb_rating=data['imDbRating'],
        metacritic_score=data['metacriticRating'],
        date_updated=date.today().strftime("%Y-%m-%d")
    )

    # make second API call. This is where streaming information will come from. Again parse data from API call with
    # .json(). Create empty list and then iterate through list of dict objects adding each dictionary to the stream_sources
    # field of media object and save.
    api_key = "bIr2F5F1XABxaT9SIJ2fBejicWI2yQGKVcepiYXY"
    url = f"https://api.watchmode.com/v1/title/{number}/sources/?apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    media.stream_sources = []
    for item in data:
        media.stream_sources.append(item)
    media.save()
    return media

# takes a request and json data. Create an empty list and then go through each item in the data adding entries and
# relevant information to be displayed to a list. Feeds the data to the paginator function, returning page object dict.

def paginate_data(request, data_to_paginate):
    data = data_to_paginate.json()
    datalist = []
    for item in data['items']:
       media = Media(id = item['id'], title = item['title'], rank = item['rank'])
       datalist.append(media)

    # creating a paginator object

    p = Paginator(datalist, 50)

    # getting the desired page number from url

    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    return {'page_obj': page_obj}

def media_detail(request, id):
    media = lookup_obj(id)
    return render(request, "movies/media_detail.html", {'data':media})

def search(request):
    name = request.POST.get('search_input')
    url = "https://imdb-api.com/en/API/SearchMovie/"
    api_key = "k_5a9rr4on/"
    response = requests.get(f"{url}{api_key}{name}")
    data = response.json()
    return render(request,"movies/movies.html", {'data':data})

def home_view(request):
    return render(request, 'movies/index.html')

def explore(request):
    return render(request, 'movies/explore.html')

def top_movies(request):
    url = "https://imdb-api.com/en/API/Top250Movies/"
    api_key = "k_5a9rr4on/"
    response = requests.get(f"{url}{api_key}")
    context = paginate_data(request, response)
    return render(request, 'movies/top_movies.html', context)

def top_tv(request):
    url = "https://imdb-api.com/en/API/Top250TVs/"
    api_key = "k_5a9rr4on/"
    response = requests.get(f"{url}{api_key}")
    context = paginate_data(request, response)
    return render(request, 'movies/top_tv.html', context)

def pop_tv(request):
    url = "https://imdb-api.com/en/API/mostpopulartvs/"
    api_key = "k_5a9rr4on/"
    response = requests.get(f"{url}{api_key}")
    context = paginate_data(request, response)
    return render(request, 'movies/pop_tv.html', context)

def pop_movies(request):
    url = "https://imdb-api.com/en/API/mostpopularmovies/"
    api_key = "k_5a9rr4on/"
    response = requests.get(f"{url}{api_key}")
    context = paginate_data(request, response)
    return render(request, 'movies/pop_movies.html', context)
