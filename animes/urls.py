from django.urls import path,include

from .views import AnimeListView,AnimeDetailView
urlpatterns = [
    path('',AnimeListView.as_view(), name='animes'),
    path('<int:pk>/', AnimeDetailView.as_view(), name='anime_detail'),
    path("api-auth/", include("rest_framework.urls")),  
]
