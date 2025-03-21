from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import movie_detail, search_movies, recommend_movies, custom_login, definition_movies, movies_by_category, \
    save_preferences, update_profile
from django.conf import settings
from django.conf.urls.static import static

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
    # path("recommend/", recommend_movies, name="recommend"),
    path("recommend/", recommend_movies, name="recommend"),
    path("definition-movies/", definition_movies, name="definition_movies"),
    path('movies/category/<str:category>/', movies_by_category, name='movies_by_category'),
    path('settings/', views.settings_view, name='settings'),
    path("edit_preferences/", save_preferences, name="save_preferences"),
    path('update-profile/', update_profile, name='update_profile'),
    path('recommend_advanced/', views.recommend_movies_advanced, name='recommend_advanced'),

       ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
