from django.urls import path
from . import views
from .views import checkout_success

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/<str:order_number>/', checkout_success, name='checkout_success'),

]