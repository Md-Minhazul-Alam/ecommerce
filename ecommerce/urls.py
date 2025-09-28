from django.contrib import admin
from django.urls import path, include

# Dev Purpose
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Tinymce
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    # Frontend URLS
    # path('', include('frontend.urls'))
    path('', include('home.urls'))
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
