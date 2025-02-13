from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import movie_detail, search_movies, recommend_movies

urlpatterns = [
    path('preferences/', views.preferences, name='preferences'),
    path('recommend/', views.recommend, name='recommend'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.signup, name='signup'),
    path('homepage/', views.homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path("recommend/", recommend_movies, name="recommend")
]

