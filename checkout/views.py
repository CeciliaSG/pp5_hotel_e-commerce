from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import SpaBookingForm
import uuid
from booking.models import SpaBookingServices
from services.models import SpaService,TimeSlot
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
import logging


# Create your views here.

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_public_key = settings.STRIPE_PUBLIC_KEY


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY


    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart")
        return redirect(reverse('home'))

    booking_id = uuid.uuid4().hex.upper()

    cart_services = []
    total_price = 0
    for unique_key, service_data in cart.items():
        try:    
            service_id, selected_date, selected_time_slot_id = unique_key.split('_')
            time_slot = TimeSlot.objects.get(pk=selected_time_slot_id)
            selected_time = time_slot.time.strftime("%H:%M")
            service = SpaService.objects.get(pk=service_id)
        except ObjectDoesNotExist:
            messages.error(request, f"The service with ID {service_id} does not exist.")
            continue
        except ValueError as e:
            logger.error(f"Error processing cart item: {e}")
            messages.error(request, f"Invalid format for cart item key: {e}")
            continue

        quantity = service_data.get('quantity', 0)
        total_price += service.price * quantity
        cart_services.append({
            'service': service,
            'quantity': quantity,
            'total_price': service.price * quantity,
            'selected_date': selected_date,
            'selected_time': selected_time,
            'selected_time_slot_id': selected_time_slot_id,
        })

        stripe_total = round(total_price * 100)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    spa_booking_form = SpaBookingForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'booking_id': booking_id,  
        'spa_booking_form': spa_booking_form,
        'cart_services': cart_services,
        'total_price': total_price,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    

    return render(request, template, context)