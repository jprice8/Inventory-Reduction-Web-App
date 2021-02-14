from django.urls import path
from . import views

urlpatterns = [

  # no intake list urls
  path('', views.no_intake_list, name='no-intake-list'),

  # api urls
  path('<int:pk>/settrue/', views.target_item_true, name='target-item-true'),
  path('<int:pk>/setfalse/', views.target_item_false, name='target-item-false'),
  path('<int:pk>/moving/', views.move_targets, name='move-targets'),

  # review target items urls
  path('review/', views.review_target_items, name='review-targets'),
  path('<int:pk>/itemplans/', views.see_item_plans, name='see-item-plans'),
]