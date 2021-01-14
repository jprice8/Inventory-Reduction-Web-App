from django.urls import path
from . import views

urlpatterns = [
    # act urls
    path('', views.act_page, name='act-page'),
]