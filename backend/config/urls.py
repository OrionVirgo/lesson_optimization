from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from api.views import schedule_interface

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR.parent / 'frontend' / 'dist')

urlpatterns += [
    re_path(r'^(?!static/|api/|admin/).*$', schedule_interface, name='home'),
]