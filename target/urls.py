from django.urls import path
from . import views

urlpatterns = [

  # target urls
  path('', views.count_usage_list, name='count-usage-list'),
]