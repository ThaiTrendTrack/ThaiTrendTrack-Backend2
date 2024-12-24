from django.urls import path
from . import views

urlpatterns = [
    path('', views.preferences, name='preferences'),  # Serve preferences page at the base URL
    path('preferences/', views.preferences, name='preferences'),
    path('recommend/', views.recommend, name='recommend')
]

