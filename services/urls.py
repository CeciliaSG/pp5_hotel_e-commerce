from django.urls import path
from . import views
from .views import (
    spa_services,
    services_by_category,
    service_details, manage_time_slots_frontend,
    availability_overview, get_time_slots_for_date)


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
    path('availability/', availability_overview,
    name='availability_overview'),
    path('manage-time-slots/<int:availability_id>/',
    manage_time_slots_frontend, name='manage_time_slots_frontend'),
    path('manage-time-slots/<int:availability_id>/get-time-slots/',
    get_time_slots_for_date, name='get_time_slots_for_date'),
    path('get-time-slots-for-date/<int:availability_id>/',
    get_time_slots_for_date, name='get_time_slots_for_date'),
    ]

