from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


def home(request):
    return JsonResponse({
        "message": "AI Ticket Management API is running",
        "status": "success"
    })

def api_health(request):
    return JsonResponse({
        "status": "success",
        "message": "Django API is connected"
    })

urlpatterns = [
    # Home / Health
    path('', home, name='home'),
  path('api/health/', api_health, name='api-health'),
    # Admin
    path('admin/', admin.site.urls),

    # OpenAPI / Swagger Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),

    # REST API Modular Endpoints
    path('api/', include('users.urls')),
    path('api/', include('customers.urls')),
    path('api/', include('agents.urls')),
    path('api/', include('tickets.urls')),
    path('api/', include('ai_engine.urls')),
    path('api/', include('analytics.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )