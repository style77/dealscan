from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from dealscan.sites import unfold_admin_site
from dealscan.views import IndexView, PricingView

urlpatterns = (
    [
        path("", IndexView.as_view(), name="index"),
        path("pricing/", PricingView.as_view(), name="pricing"),
        path("admin/", unfold_admin_site.urls),
        path("accounts/", include("accounts.urls")),
        path("subscriptions/", include("billing.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEBUG:
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
