from django.urls import path
from . import views

app_name = 'search_app'  # Changed 'search-app' to 'search_app'
urlpatterns = [
    path('', views.SearchResult, name='SearchResult'),  # Changed 'SeachResult' to 'SearchResult'
]
