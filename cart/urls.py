from django.urls import path
from . import views

'''
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add<product_id>/', views.cart_add, name='cart_add'),
    path('remove<product_id>/', views.cart_remove, name='cart_remove'),
]
'''
app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:St_id>/',
         views.cart_add,
         name='cart_add'),
    path('remove/<int:St_id>/',
         views.cart_remove,
         name='cart_remove'),
]