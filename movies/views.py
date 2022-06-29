from django.shortcuts import render
import requests



def movie_detail(request, id):
    api_key = "bIr2F5F1XABxaT9SIJ2fBejicWI2yQGKVcepiYXY"
    url = f"https://api.watchmode.com/v1/title/{id}/sources/?apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    return render(request, "movies/movie_detail.html",{'data':data})

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
    return render(request, 'movies/top_movies.html')

def top_tv(request):
    return render(request, 'movies/top_tv.html')

def pop_tv(request):
    return render(request, 'movies/pop_tv.html')

def top_movies(request):
    return render(request, 'movies/pop_movies.html')