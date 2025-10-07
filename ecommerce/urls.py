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
    # Frontend URLs
    # path('', include('frontend.urls'))
    path('', include('home.urls')),
    path('products/', include('product.urls')),
    path('bag/', include('bag.urls')),
]

# Serve static + media files during development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
