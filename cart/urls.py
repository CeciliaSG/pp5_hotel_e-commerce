from django.urls import path
from . import views
from .views import (add_to_cart, view_cart, 
clear_cart, update_cart, remove_from_cart)


urlpatterns = [
    #path('add_to_cart/<int:booking_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update_cart/<str:service_id>/', update_cart, name='update_cart'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('remove_from_cart/<str:service_id>/', views.remove_from_cart, name='remove_from_cart'),
]