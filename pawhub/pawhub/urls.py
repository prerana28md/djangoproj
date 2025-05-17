from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('pets/', include('pets.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('users/', include('users.urls')),
    path('lost-found/', include('lost_found.urls')),
    path('hospitals/', include('hospitals.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
