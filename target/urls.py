from django.urls import path
from . import views

urlpatterns = [

  # target urls
  path('', views.count_usage_list, name='count-usage-list'),
  path('<int:pk>/settrue/', views.target_item_true, name='target-item-true'),
  path('<int:pk>/setfalse/', views.target_item_false, name='target-item-false'),
  path('<int:pk>/moving/', views.move_targets, name='move-targets'),
  path('review/', views.review_target_items, name='review-targets'),
]