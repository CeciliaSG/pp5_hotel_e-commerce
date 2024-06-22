from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    #path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('', views.profile, name='customer_profile'),
    path('booking_history/<booking_number>', views.booking_history, name='booking_history'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),

]