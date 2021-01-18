from django.urls import path
from . import views

urlpatterns = [

  # target urls
  path('', views.count_usage_list, name='count-usage-list'),
  path('api/listing/', views.ajax_post_target, name='target-api-listing'),
  path('api/reduction/', views.ajax_reduction_qty, name='target-api-reduction'),
  path('<int:pk>/moving/', views.move_targets, name='move-targets'),
]