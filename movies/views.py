from django.shortcuts import render
import requests
from .models import Movie
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def save_movie(request, number):
    Movie.objects.get_or_create(id = number)
    if request.user.is_active:
        user = request.user
        response = user.profile.watchlist.get('data')
        if user.profile.watchlist:
            response.append(number)
            user.profile.watchlist = {'data': response}
        else:
            user.profile.watchlist.update({'data': [number]})
        user.save()
    return render(request, 'movies/index.html')


def movie_detail(request, id):
    api_key = "k_5a9rr4on"
    url = f"https://imdb-api.com/en/API/Title/{api_key}/{id}"
    response = requests.get(url)
    data = response.json()
    return render(request, "movies/movie_detail.html", {'data':data})


def sources(request, id):
    api_key = "bIr2F5F1XABxaT9SIJ2fBejicWI2yQGKVcepiYXY"

    url = f"https://imdb-api.com/en/API/Title/{api_key}/{id}"
    response = requests.get(url)
    data = response.json()
    return render(request, "movies/sources.html", {'data': data})

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

def top_movies(request, page):
    url = "https://imdb-api.com/en/API/Top250Movies/"
    api_key = "k_5a9rr4on/"
    response = requests.get(f"{url}{api_key}")
    data = response.json()
    return render(request, 'movies/top_movies.html', {'data':data})

def top_tv(request):
    url = "https://imdb-api.com/en/API/Top250TVs/"
    api_key = "k_5a9rr4on/"
    response = requests.get(f"{url}{api_key}")
    data = response.json()
    return render(request, 'movies/top_tv.html', {'data':data})

def pop_tv(request):
    url = "https://imdb-api.com/en/API/mostpopulartvs/"
    api_key = "k_5a9rr4on/"
    response = requests.get(f"{url}{api_key}")
    data = response.json()
    return render(request, 'movies/pop_tv.html', {'data':data})

def pop_movies(request):
    url = "https://imdb-api.com/en/API/mostpopularmovies/"
    api_key = "k_5a9rr4on/"
    response = requests.get(f"{url}{api_key}")
    data = response.json()
    return render(request, 'movies/pop_movies.html', {'data':data})

def listing(request):
    url = "https://imdb-api.com/en/API/Top250TVs/"
    api_key = "k_5a9rr4on/"
    response = requests.get(f"{url}{api_key}")
    data = response.json()
    data_list = list(data.values())
    p = Paginator(data_list, 5)  # creating a paginator object
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

    return render(request, 'movies/top_movies.html',{'page_obj': page_obj})