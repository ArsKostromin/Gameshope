from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.profiles, name="profiles"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('edit-account/', views.editAccount, name="edit-account"),
    path('account/', views.userAccount, name="account"),
    path('logout/', views.logoutUser, name="logout"),
    path('login/', views.loginUser, name="login"),
    path('register/', views.registerUser, name="register"), 
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




    
    # path('register/', views.registerUser, name="register"),  
    # path('account/', views.userAccount, name="account"),
    # я