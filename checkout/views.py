from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.urls import reverse
from .forms import SpaBookingForm
from accounts.forms import CustomerProfileForm
from booking.forms import ServiceBookingForm
import uuid
from booking.models import SpaBooking, SpaBookingServices
from accounts.models import CustomerProfile
from services.models import SpaService,TimeSlot
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
import logging
from datetime import datetime
from django.utils import timezone
import json
from django.views.decorators.http import require_POST



# Create your views here.

logger = logging.getLogger(__name__)

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    print("Session data before adding items:", request.session.get('cart', {}))

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
    stripe.api_key = stripe_secret_key
    logger.debug("Cart data: %s", cart)
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
        payment_method_types=['card'],
        confirm=False,
        metadata={
        'cart': json.dumps(cart),
        }
    )

    spa_booking_form = SpaBookingForm()
    if request.method == 'POST':
        spa_booking_form = SpaBookingForm(request.POST)
        if spa_booking_form.is_valid():
            spa_booking = spa_booking_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            spa_booking.stripe_pid = pid
            spa_booking.original_cart = json.dumps(cart)
            #spa_booking.save()

            customer_name = spa_booking_form.cleaned_data['customer_name']
            email = spa_booking_form.cleaned_data['email']
            phone_number = spa_booking_form.cleaned_data['phone_number']

            if cart_services:
                first_service = cart_services[0]
                selected_date = datetime.strptime(first_service['selected_date'], "%B %d, %Y").date()
                selected_time = datetime.strptime(first_service['selected_time'], "%H:%M").time()
                date_and_time = datetime.combine(selected_date, selected_time)
                date_and_time = timezone.make_aware(date_and_time)
            else:
                date_and_time = datetime.now()

            spa_booking.date_and_time = date_and_time
            spa_booking.booking_total = total_price
            spa_booking.stripe_pid = request.POST.get('stripe_pid', '')
            spa_booking.save()

            #spa_booking = SpaBooking.objects.create(
                #customer_name=customer_name,
                #email=email,
                #phone_number=phone_number,
                #date_and_time=date_and_time,
                #booking_total=total_price,
                #stripe_pid=request.POST.get('stripe_pid', '')
            #)

            for cart_service in cart_services:
                spa_service = cart_service['service']
                quantity = cart_service['quantity']
                spa_service_total = cart_service['total_price']
                selected_date = datetime.strptime(cart_service['selected_date'], "%B %d, %Y").date()
                selected_time = datetime.strptime(cart_service['selected_time'], "%H:%M").time()
                selected_time_slot_id = cart_service['selected_time_slot_id']
                selected_datetime = datetime.combine(selected_date, selected_time)


                spa_booking_service = SpaBookingServices.objects.create(
                    spa_service=spa_service,
                    quantity=quantity,
                    spa_service_total=spa_service_total,
                    spa_booking=spa_booking,
                    date_and_time=selected_datetime,
                )
                selected_datetime = timezone.make_aware(selected_datetime)
                
                request.session['save_info'] = 'save-info' in request.POST
            else:
                messages.error(request, 'There was an error with your form. Please double check your information.')


                return redirect(reverse('checkout_success', kwargs={'booking_number': spa_booking.booking_number}))

    else:
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
        'messages': messages.get_messages(request),
        'cart':cart,
    }

    return render(request, template, context)


@require_POST
def cache_checkout_data(request):
    """
    From Ado walkthrough. 
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, "Unfortuately, your payment can't be \
            processed at the moment. Please try again later.")
        return HttpResponse(content=e, status=400)


def checkout_success(request, booking_number):
    """
    From Ado walkthrough. Handle successful checkouts
    """

    save_info = request.session.get('save_info')
    booking = get_object_or_404(SpaBooking, booking_number=booking_number)

    if request.user.is_authenticated:
        user = request.user
        profile = CustomerProfile.objects.get(user=request.user)
        booking.customer_profile = profile
        booking.save()

    if save_info:
        profile_data = {
            'deafailt_email': booking.email,
            'default_phone_number': booking.phone_number,
        }
        customer_profile_form = CustomerProfileForm(profile_data, instance=profile)
        if customer_profile_form.is_valid():
            customer_profile_form.save()
        
        user.email = booking.email
        user.save()

    messages.success(request, f'Order successfully processed! \
        Your booking number is {booking_number}. A confirmation \
        email will be sent to {booking.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'booking': booking,
        'messages': messages.get_messages(request),
    }

    return render(request, template, context)    