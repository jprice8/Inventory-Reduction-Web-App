from django.urls import path
from . import views
from .views import ItemsWithNoIntakeTableView, ItemsWithIntakeTableView

urlpatterns = [
    # act urls
    path('', views.act_page, name='act-page'),

    # API urls
    path('<int:pk>/resulthandler/', views.result_handler, name='result-handler'),
    path('<int:pk>/acceptqtyhandler/', views.accept_qty_handler, name='accept-qty-handler'),
    path('<int:pk>/finalizeplanhandler/', views.finalize_plan_handler, name='finalize-plan'),

    # review to export out plans
    path('review/nointaketable/', ItemsWithNoIntakeTableView.as_view(), name='review-nointake'),
    path('review/intake/', ItemsWithIntakeTableView.as_view(), name='review-intake'),
    path('review/targets/', views.review_targets, name='review-targeted'),
    path('review/completed/', views.review_completed, name='review-completed'),
    path('review/completed/export/', views.completed_export_excel, name='export-completed'),
    path('review/accepted/', views.review_accepted, name='review-accepted'),
    path('review/accepted/export/', views.accepted_export_excel, name='export-accepted'),

    # generic class views for editing movement plans
    path('<int:pk>/itemplans/edit/', views.MovementPlanUpdate.as_view(), name='edit-plan'),
    path('<int:pk>/itemplans/delete/', views.MovementPlanDelete.as_view(), name='delete-plan'),
]