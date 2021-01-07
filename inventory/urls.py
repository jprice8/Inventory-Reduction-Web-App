from django.urls import path
from . import views

urlpatterns = [
  # landing page
  path('', views.index, name='index'),

  # inventory urls
  path('inventory/', views.inventory_list, name='inventory-list'),
]