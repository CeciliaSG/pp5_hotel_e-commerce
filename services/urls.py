from django.urls import path
from . import views
from .views import (
    spa_services,
    services_by_category,
    service_details)


urlpatterns = [
    path('', views.spa_services, name='spa_services'),
    path(
        'category/<int:category_id>/',
        views.services_by_category,
        name='services_by_category'
    ),
    path(
        'service/<int:service_id>/',
        service_details,
        name='service_details'
    ), 

    path('service/<int:service_id>/edit_review/<int:review_id>',
     views.review_edit, name='review_edit'),
    path('service/<int:service_id>/delete_review/<int:review_id>',
     views.review_delete, name='review_delete'),

    ]

