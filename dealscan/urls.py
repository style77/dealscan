from django.conf import settings
from .sites import unfold_admin_site
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path("admin/", unfold_admin_site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
