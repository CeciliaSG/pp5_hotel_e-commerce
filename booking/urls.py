from django.urls import path
from . import views
from .views import book_spa_service

urlpatterns = [
 path('book_spa_service/<int:service_id>/', views.book_spa_service, name='book_spa_service'),
]