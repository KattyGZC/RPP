from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import LoginView, LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    # JWT Auth
    path("api/auth/login/", LoginView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/logout/", LogoutView.as_view(), name="token_blacklist"),
    # App routes
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/exercises/", include("apps.exercises.urls")),
    path("api/evaluation/", include("apps.evaluation.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
