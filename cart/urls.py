from django.urls import path
from . import views
from .views import add_to_cart, view_cart


urlpatterns = [
    path('add_to_cart/<int:booking_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
]