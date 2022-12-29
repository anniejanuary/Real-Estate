from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenRefreshView
from user_api.views import MyObtainTokenPairView

urlpatterns = [
    # Token endpoints
    path(
        "api/token/",
        MyObtainTokenPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
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
