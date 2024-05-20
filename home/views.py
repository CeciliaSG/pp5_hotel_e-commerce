from django.shortcuts import render
from booking.views import book_spa_service
from services.views import spa_services


# Create your views here.

def index(request):
    """
    Renders index template
    """

    booking_context = book_spa_service(request)
    services_context = spa_services(request)

    context = {
        'booking_context': booking_context,
        'services_context': services_context,
    }

    return render(request, 'home/index.html', context)
