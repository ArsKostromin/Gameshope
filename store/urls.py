from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from .views import by_genre, StoreListView, StoreDetailView, PublisherDetailView, GametViewSet, GetGenreInfoView, GetPublisherInfoView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('genre-<slug:genre_slug>', by_genre, name='by_genre'),
    path('', StoreListView.as_view(), name='index'),
    path('publisher-<slug>', PublisherDetailView.as_view(), name='publisher-detail'),
    path('<slug>', StoreDetailView.as_view(), name='st-detail'),
]

router = DefaultRouter()
router.register(r'game', GametViewSet, basename="game")

api_urlpatterns = [
    path('api/genre/', GetGenreInfoView.as_view(), name='APIgenre'),
    path('api/publisher/', GetPublisherInfoView.as_view(), name='APIpublisher'),
    path('api/', include(router.urls)),
    ]

urlpatterns += api_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)