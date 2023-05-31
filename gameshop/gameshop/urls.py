from django.conf import settings
from django.conf.urls.static import static
from re import I
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('store/', include('store.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
'''
urlpatterns += [
    path('admin/', include(admin.site.urls)),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('shop.urls', namespace='shop')),
]
'''