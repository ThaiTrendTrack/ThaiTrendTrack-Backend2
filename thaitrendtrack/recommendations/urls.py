from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import movie_detail, search_movies, recommend_movies, custom_login

urlpatterns = [
    path('preferences/', views.preferences, name='preferences'),
    path('recommend/', views.recommend, name='recommend'),
    path('login/', custom_login, name='login'),
    path('signup/', views.login_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.signup, name='signup'),
    path('homepage/', views.homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path("recommend/", recommend_movies, name="recommend")
]

