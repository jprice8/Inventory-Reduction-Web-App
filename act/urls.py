from django.urls import path
from . import views

urlpatterns = [
    # act urls
    path('', views.act_page, name='act-page'),
    path('<int:pk>/resulthandler/', views.result_handler, name='result-handler'),
    path('<int:pk>/acceptqtyhandler/', views.accept_qty_handler, name='accept-qty-handler'),
    path('review/accepted/', views.review_accepted, name='review-accepted'),
]