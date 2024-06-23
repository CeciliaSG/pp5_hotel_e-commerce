from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='customer_profile'),
    path('booking_history/<booking_number>', views.booking_history, name='booking_history'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),

]