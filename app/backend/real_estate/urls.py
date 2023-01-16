from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from user_api.views import (
    MyTokenBlacklistView,
    MyTokenObtainPairView,
    MyTokenRefreshView,
)

urlpatterns = [
    # Auth endpoints - JWTs in httponly cookies
    path(
        "api/auth/login/",
        MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/auth/refresh/",
        MyTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/auth/logout/",
        MyTokenBlacklistView.as_view(),
        name="token_blacklist",
    ),
    # Admin panel endpoint
    path("admin/", admin.site.urls),
    # Docs endpoints
    path(
        "api/schema/", SpectacularAPIView.as_view(), name="api-schema"
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    # All user_api.urls endpoints included
    path("api/user/", include("user_api.urls")),
]
