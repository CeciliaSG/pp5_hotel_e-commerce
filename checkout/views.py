from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import SpaBookingForm
import uuid
from booking.models import SpaBookingServices
from services.models import SpaService


# Create your views here.

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart")
        return redirect(reverse('home'))

    booking_id = uuid.uuid4().hex.upper()

    cart_services = []
    total_price = 0
    for service_id, service_data in cart.items():
        service = SpaService.objects.get(pk=service_id)
        quantity = service_data.get('quantity', 0)
        total_price += service.price * quantity
        cart_services.append({
            'service': service,
            'quantity': quantity,
            'total_price': service.price * quantity
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