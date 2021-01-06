from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # admin urls
    path('admin/', admin.site.urls),

    # inventory urls
    path('', include('inventory.urls')),
]
