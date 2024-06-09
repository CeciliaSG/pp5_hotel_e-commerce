from django.urls import path
from . import views
from .views import checkout_success
from .webhooks import webhook

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/checkout_success/<str:booking_number>/', checkout_success, name='checkout_success'),
    path('wh/', webhook, name='webhook'),


]