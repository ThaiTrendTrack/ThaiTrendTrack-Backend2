from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import recommend_movies, custom_login, definition_movies, movies_by_category, \
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
    path('community/', views.community_home, name='community_home'),
    path('community/<int:community_id>/post/', views.create_post, name='create_post'),
    path('community/<int:community_id>/create/', views.create_post, name='create_post'),
    path('community/<int:community_id>/', views.community_home, name='community_home'),
    path('post/<int:post_id>/comment/', views.comment_on_post, name='comment_on_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('hashtag/<str:hashtag_name>/', views.hashtag_posts, name='hashtag_posts'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('recommend_advanced/', views.recommend_movies_advanced, name='recommend_advanced'),
    path('movies_advance/', views.movies_advance, name='movies_advance'),

       ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
