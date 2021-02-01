from django.urls import path
from . import views

urlpatterns = [
    # act urls
    path('', views.act_page, name='act-page'),

    # API urls
    path('<int:pk>/resulthandler/', views.result_handler, name='result-handler'),
    path('<int:pk>/acceptqtyhandler/', views.accept_qty_handler, name='accept-qty-handler'),

    # review to export out plans
    path('review/accepted/', views.review_accepted, name='review-accepted'),
    path('review/accepted/export/', views.accepted_export_excel, name='export-accepted'),
    path('review/completed/', views.review_completed, name='review-completed'),
    path('review/completed/export/', views.completed_export_excel, name='export-completed'),

    # view all requests
    path('requests/', views.view_requests, name='view-requests'),
]