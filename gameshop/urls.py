from django.conf import settings
from django.conf.urls.static import static
from re import I
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
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

