import logging
import traceback
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.templatetags.static import static as static_url
from django.template.response import TemplateResponse

logger = logging.getLogger('works')


# Ограничиваем Django admin только суперпользователями (не просто is_staff)
_original_has_permission = admin.site.__class__.has_permission


def _superuser_only(self, request):
    return request.user.is_active and request.user.is_superuser


admin.site.__class__.has_permission = _superuser_only  # type: ignore[method-assign]


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


def _hidden_admin_404(request, *args, **kwargs):
    raise Http404


urlpatterns = [
    path('admin/', _hidden_admin_404),               # старый /admin/ → 404 для всех
    path('cp-secure-2025/', admin.site.urls),        # реальная панель — только суперы
    path('', include('works.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('favicon.ico', favicon, name='favicon'),
    path('.well-known/<path:path>', handle_chrome_devtools, name='chrome_devtools'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
