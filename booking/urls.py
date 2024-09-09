from django.urls import path
from .views import book_spa_service, get_available_dates

urlpatterns = [
    path("book_spa_service/", book_spa_service, name="book_spa_service"),
    path('get-available-dates/<int:service_id>/', get_available_dates, name='get_available_dates'),
]
