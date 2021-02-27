from django.urls import path
from . import views

urlpatterns = [
    # leaderboard urls
    path('', views.leaderboard, name='leaderboard'),
]