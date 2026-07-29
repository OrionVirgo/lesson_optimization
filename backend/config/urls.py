from django.contrib import admin
from django.urls import path, include
from api.views import schedule_interface

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', schedule_interface, name='home'),
]