from datetime import datetime
from dateutil import parser
import json

import stripe
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    HttpResponse,
)
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import SpaBookingForm
from accounts.forms import CustomerProfileForm
from booking.forms import ServiceBookingForm
from accounts.models import CustomerProfile
from booking.models import SpaBooking, SpaBookingServices
from services.models import SpaService, TimeSlot, SpecificDate, Availability
#import uuid

from django.http import HttpResponse, JsonResponse
import json

# Create your views here.

def parse_date(date_str):
    """
    Parse the date string and return a date object.
    """
    try:
        return datetime.strptime(date_str, "%B %d, %Y").date()
    except ValueError:
        return parser.parse(date_str).date()


@require_POST
def cache_checkout_data(request):
    """
    From Boutique Ado walkthrough.

    Caches checkout data in Stripe PaymentIntent metadata.

    This view function is responsible for updating the Stripe PaymentIntent
    with additional metadata before the payment is processed. The metadata
    includes the user's cart contents, whether the user wants to save their
    information for future use, and the username of the user making the
    purchase.

    The function retrieves the PaymentIntent ID from the 'client_secret'
    in the POST data, extracts the cart data from the session, and updates
    the PaymentIntent with this metadata. If an error occurs during this
    process, an error message is displayed to the user.

    Args:
        request (HttpRequest): The HTTP request object containing the
        POST data.

    Returns:
        HttpResponse: A response with HTTP status 200 if the metadata is
        successfully cached, or an error response with HTTP status 400
        if an exception occurs.

    Raises:
        Exception: Any exception that occurs during the modification of
        the PaymentIntent is caught and results in an error response.
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY

        stripe.PaymentIntent.modify(pid, metadata={
            'save_info': request.POST.get('save_info'),
            'username': str(request.user),
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, "Unfortunately, your payment can't be "
                       "processed at the moment. Please try again later.")

        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    Handle the checkout process for spa services, including payment via Stripe.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your cart")
            return redirect(reverse('home'))

        form_data = {
            'customer_name': request.POST['customer_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
        }
        spa_booking_form = SpaBookingForm(form_data)
        if spa_booking_form.is_valid():
            spa_booking = spa_booking_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            spa_booking.stripe_pid = pid
            spa_booking.original_cart = json.dumps(cart)
            
            cart_services = []
            total_price = 0
            date_and_time = None
            for unique_key, service_data in cart.items():
                try:
                    service_id, selected_date, selected_time_slot_id = unique_key.split('_')
                    time_slot = TimeSlot.objects.get(pk=selected_time_slot_id)
                    selected_time = time_slot.time.strftime("%H:%M")
                    service = SpaService.objects.get(pk=service_id)
                except ObjectDoesNotExist:
                    messages.error(request, f"The service with ID {service_id} does not exist.")
                    return redirect(reverse('home'))
                except ValueError as e:
                    messages.error(request, f"Invalid format for cart item key: {e}")
                    return redirect(reverse('home'))

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

                if not date_and_time:
                    selected_date_obj = parse_date(selected_date)
                    selected_time_obj = datetime.strptime(selected_time, "%H:%M").time()
                    date_and_time = timezone.make_aware(datetime.combine(selected_date_obj, selected_time_obj))

            spa_booking.booking_total = total_price
            spa_booking.date_and_time = date_and_time
            spa_booking.save()

            for cart_service in cart_services:
                spa_service = cart_service['service']
                quantity = cart_service['quantity']
                spa_service_total = cart_service['total_price']
                selected_date = parse_date(cart_service['selected_date'])
                selected_time = datetime.strptime(cart_service['selected_time'], "%H:%M").time()
                selected_datetime = datetime.combine(selected_date, selected_time)
                selected_datetime = timezone.make_aware(selected_datetime)

                SpaBookingServices.objects.create(
                    spa_service=spa_service,
                    quantity=quantity,
                    spa_service_total=spa_service_total,
                    spa_booking=spa_booking,
                    date_and_time=selected_datetime,
                )

                time_slot = TimeSlot.objects.get(pk=cart_service['selected_time_slot_id'])

                specific_dates = SpecificDate.objects.filter(date=selected_date, timeslotavailability__time_slot=time_slot)

                if specific_dates.exists():
                    specific_date = specific_dates.first()

                    print(f"Matching SpecificDate found: {specific_date.date} (ID: {specific_date.id})")

                    print(f"Marking TimeSlot {time_slot.time} as unavailable for SpecificDate {specific_date.date}")

                    time_slot.mark_unavailable_for_date(specific_date)
                else:
                    print(f"No matching SpecificDate found for {selected_date} and TimeSlot {time_slot.time}")


            request.session['save_info'] = 'save-info' in request.POST

            request.session['customer_name'] = form_data['customer_name']
            request.session['email'] = form_data['email']
            request.session['phone_number'] = form_data['phone_number']

            return redirect(reverse('checkout_success', args=[spa_booking.booking_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')

    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your cart")
            return redirect(reverse('home'))

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
                return redirect(reverse('home'))
            except ValueError as e:
                messages.error(request, f"Invalid format for cart item key: {e}")
                return redirect(reverse('home'))

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

        customer_name = request.session.get('customer_name', 'Not provided')
        email = request.session.get('email', 'Not provided')
        phone_number = request.session.get('phone_number', 'Not provided')
        booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        metadata = {
            'username': request.user.username if request.user.is_authenticated else '',
            'save_info': request.session.get('save_info', False),
            'booking_total': total_price,
            'booking_date': booking_date,
            'customer_name': customer_name,
            'email': email,
            'phone_number': phone_number,
        }
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
            metadata=metadata,
        )

        spa_booking_form = SpaBookingForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'spa_booking_form': spa_booking_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'cart_services': cart_services,
        'total_price': total_price,
        'messages': messages.get_messages(request),
        'cart': cart,
    }

    return render(request, template, context)


def checkout_success(request, booking_number):
    """
    Handle successful checkout completion and display
    the checkout success page.

    Retrieves booking details based on the provided `booking_number`.
    If the user is authenticated, associates the booking with the user's
    customer profile.
    If 'save_info' is set in session, updates user and customer profile
    information with booking details.
    Displays a success message with the booking number and email.
    Clears the 'cart' from session after successful checkout.

    Args:
        request (HttpRequest): The HTTP request object.
        booking_number (str): The unique booking number identifying
        the completed booking.

    Returns:
        HttpResponse: Rendered template with booking details
        and success message.

    Raises:
        Http404: If no booking exists with the provided `booking_number`.
    """
    save_info = request.session.get('save_info')
    booking = get_object_or_404(SpaBooking, booking_number=booking_number)
    services = SpaBookingServices.objects.filter(spa_booking=booking)


    if request.user.is_authenticated:
        user = request.user
        profile, created = CustomerProfile.objects.get_or_create(user=request.user)
        booking.customer_profile = profile
        booking.save()

        if save_info:
            profile_data = {
                'email': booking.email,
                'default_phone_number': booking.phone_number,
            }
            customer_profile_form = CustomerProfileForm(profile_data, instance=profile)
            if customer_profile_form.is_valid():
                customer_profile_form.save()

            user.email = booking.email
            user.save()

    messages.success(request, f'Order successfully processed! Your booking number is {booking_number}. A confirmation email will be sent to {booking.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'booking': booking,
        'services': services,
    }

    return render(request, template, context)


