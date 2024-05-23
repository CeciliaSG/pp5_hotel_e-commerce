from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import SpaBookingForm



# Create your views here.

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart")
        return redirect(reverse('home'))

    spa_booking_form = SpaBookingForm()
    template = 'checkout/checkout.html'
    context = {
        'spa_booking_form': spa_booking_form,
    }

    return render(request, template, context)