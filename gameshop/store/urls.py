from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from .views import by_genre, StoreListView, StoreDetailView, PublisherDetailView, LoanedStsByUserListView, SignUp
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [   
    path('<int:genre_id>', by_genre, name = 'by_genre'),
    path('', StoreListView.as_view(), name = 'index'),
    path('game<int:pk>', StoreDetailView.as_view(), name='st-detail'),
    path('publisher<int:pk>', PublisherDetailView.as_view(), name='publisher-detail'),
    path('mygames/', LoanedStsByUserListView.as_view(), name='my-borrowed'),
    path('signup/', SignUp.as_view(), name="signup")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

