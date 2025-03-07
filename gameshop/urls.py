from django.conf import settings
from django.conf.urls.static import static
from re import I
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Документация для gameshop",
        default_version="v1",
        description="Документация для API проекта",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
    path('store/', include('store.urls')),
    path('cart', include('cart.urls', namespace='cart')),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
]

urlpatterns += [
    path('', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns

