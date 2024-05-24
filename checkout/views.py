from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import SpaBookingForm
import uuid
from booking.models import SpaBookingServices
from services.models import SpaService
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart")
        return redirect(reverse('home'))

    booking_id = uuid.uuid4().hex.upper()

    cart_services = []
    total_price = 0
    for unique_key, service_data in cart.items():
        try:    
            service_id, selected_date_and_time = unique_key.split('_')            
            service = SpaService.objects.get(pk=service_id)
        except ObjectDoesNotExist:
            messages.error(request, f"The service with ID {service_id} does not exist.")
            continue

        quantity = service_data.get('quantity', 0)
        total_price += service.price * quantity
        cart_services.append({
            'service': service,
            'quantity': quantity,
            'total_price': service.price * quantity,
            "selected_date_and_time": service_data.get("selected_date_and_time", "N/A"),

        })

    spa_booking_form = SpaBookingForm()
    template = 'checkout/checkout.html'
    context = {
        'booking_id': booking_id,  
        'spa_booking_form': spa_booking_form,
        'cart_services': cart_services,
        'total_price': total_price,
    }

    return render(request, template, context)