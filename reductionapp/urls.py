from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from users import views as user_views

urlpatterns = [
    # admin urls
    path('admin/', admin.site.urls),

    # auth urls
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # inventory urls
    path('', include('inventory.urls')),

    # target urls
    path('target/', include('target.urls')),

    # act urls
    path('act/', include('act.urls')),
]
