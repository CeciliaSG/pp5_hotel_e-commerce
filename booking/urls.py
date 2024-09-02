from django.urls import path
from .views import book_spa_service

urlpatterns = [
    path("book_spa_service/", book_spa_service, name="book_spa_service"),
]

