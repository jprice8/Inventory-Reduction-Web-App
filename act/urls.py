from django.urls import path
from . import views
from .views import ItemsWithNoIntakeTableView, ItemsWithIntakeTableView, ReviewTargetedItemsTableView, ReviewCompletedPlansTableView, ReviewAcceptedPlansTableView

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
    path('review/targets/', ReviewTargetedItemsTableView.as_view(), name='review-targeted'),
    path('review/completed/', ReviewCompletedPlansTableView.as_view(), name='review-completed'),
    path('review/accepted/', ReviewAcceptedPlansTableView.as_view(), name='review-accepted'),

    # generic class views for editing movement plans
    path('<int:pk>/itemplans/edit/', views.MovementPlanUpdate.as_view(), name='edit-plan'),
    path('<int:pk>/itemplans/delete/', views.MovementPlanDelete.as_view(), name='delete-plan'),
]