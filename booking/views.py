from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import SpaBookingForm, SpaBookingServicesFormSet
from .models import SpaBooking, SpaBookingServices, SpaService
from datetime import datetime
from django.urls import reverse


# Create your views here.

def book_spa_service(request, service_id):
    service = get_object_or_404(SpaService, pk=service_id)
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url', 'view_cart')
    cart = request.session.get('cart', {})
    service_id_str = str(service_id)

    if service_id_str in cart:
        cart[service_id_str]['quantity'] += quantity
        cart[service_id_str]['spa_service_total'] = str(service.price * cart[service_id_str]['quantity'])
        messages.success(request, f'Updated {service.name} quantity to {cart[service_id_str]["quantity"]}')
    else:
        cart[service_id_str] = {
            'spa_service': service.name,
            'quantity': quantity,
            'spa_service_total': str(service.price * quantity)
        }
        messages.success(request, f'Added {service.name} to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)






    


