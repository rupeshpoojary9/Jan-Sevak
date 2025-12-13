from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    # The Admin Panel
    path('admin/', admin.site.urls),
    
    # The API Routes
    path('api/', include('complaints.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # Serve React Frontend (Catch-all)
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)