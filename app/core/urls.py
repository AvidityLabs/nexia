"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

def trigger_error(request):
    division_by_zero = 1 / 0
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('llm/v1/', include(('llm.urls', 'llmv1'), namespace='lmmv1')),# All endpoints 
    path('api/v1/', include(('core.api_v1_urls', 'apiv1'), namespace='apiv1')),# All endpoints 
    # OpenAPI 3 documentation with Swagger UI
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(template_name="swagger-ui.html", url_name="schema"),name="swagger-ui",),
    path('api/v2/usecases/', include(('usecases.urls', 'usecases_v1'), namespace='usecases_v1')),# All endpoints 
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'core.settings.dev':
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')),)
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'core.settings.prod':
    urlpatterns.append(path('sentry-debug/', trigger_error),)
# If using Docker the following will set your INTERNAL_IPS correctly in Debug mode:
# if DEBUG:
#     import socket  # only if you haven't already imported this
#     hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#     INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
