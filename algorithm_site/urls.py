import logging
import traceback
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, HttpResponseRedirect
from django.templatetags.static import static as static_url
from django.template.response import TemplateResponse

logger = logging.getLogger('works')

def handle_chrome_devtools(request):
    return HttpResponse('', status=404)

def favicon(request):
    return HttpResponseRedirect(static_url('works/favicon.png'))

def handler500_view(request):
    exc = traceback.format_exc()
    logger.error(
        'Internal Server Error: %s\nUser: %s\nMethod: %s\nPOST: %s\n%s',
        request.path,
        getattr(request, 'user', 'unknown'),
        request.method,
        dict(request.POST) if request.method == 'POST' else '-',
        exc,
    )
    return TemplateResponse(request, '500.html', status=500)

def handler404_view(request, exception=None):
    logger.warning('Page not found: %s (user=%s)', request.path,
                   getattr(request, 'user', 'unknown'))
    return TemplateResponse(request, '404.html', status=404)

handler500 = handler500_view
handler404 = handler404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('works.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('favicon.ico', favicon, name='favicon'),
    path('.well-known/<path:path>', handle_chrome_devtools, name='chrome_devtools'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
