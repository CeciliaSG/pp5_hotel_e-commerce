from django.urls import path
from . import views
from .views import checkout_success

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/checkout_success/<str:booking_number>/', checkout_success, name='checkout_success'),

]