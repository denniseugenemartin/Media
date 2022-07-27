from django.urls import path,include
from . import views

urlpatterns = [
    path('login_user/', views.login_user, name = 'login_request'),
    path('logout_user/', views.logout_user, name = 'logout_request'),
    path("register/", views.register_user, name="register_request"),
    path("about/", views.about, name = 'about'),
    path("watchlist/", views.watchlist, name = 'watchlist'),
    path(r'remove_media/<str:number>/', views.remove_media, name='remove_media'),
    path(r'save_movie/<str:number>/', views.save_media, name='save_movie')
    ]
