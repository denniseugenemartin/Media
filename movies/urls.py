from django.contrib import admin
from django.urls import path, include
from movies import views


urlpatterns = [

    path(r'movie_detail/<str:id>/', views.movie_detail, name = 'detail'),
    path('admin/', admin.site.urls),
    path('search/', views.search, name ='search'),
    path('', views.home_view, name = "home"),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('explore/', views.explore, name = 'explore'),
    path('top_movies/', views.top_movies, name = 'top_movies'),
    path('top_tv/', views.top_tv, name='top_tv'),
    path('pop_tv/', views.pop_tv, name='pop_tv'),
    path('pop_movies/', views.pop_tv, name='pop_movies')


    ]
