import json
import time
from datetime import datetime

import uuid
import stripe

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.utils.timezone import make_aware, get_current_timezone

from booking.models import SpaBooking, SpaBookingServices
from services.models import SpaService, TimeSlot


class StripeWH_Handler:
    """
    Handle Stripe webhooks from Boutique Ado walkthrough.

    Attributes:
        request (HttpRequest): The HTTP request object
        received from Stripe.

    Methods:
        __init__(self, request):
            Initialize with the incoming HTTP request
            from Stripe.

        _send_confirmation_email(self, spa_booking):
            Send a confirmation email to the user for
            a spa booking.

            Args:
                spa_booking (SpaBooking): The spa booking
                instance containing details.

            Raises:
                Exception: If there is an issue sending the email.
    """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, spa_booking, services):
        """From Boutique Ado. Send the user a confirmation email."""

        cust_email = None
        try:
            cust_email = spa_booking.email
            subject = render_to_string(
                'checkout/confirmation_emails/confirmation_email_subject.txt',
                {'booking': spa_booking})
            body = render_to_string(
                'checkout/confirmation_emails/confirmation_email_body.txt',
                {'spa_booking': spa_booking,
                    'services': services,
                    'contact_email': settings.DEFAULT_FROM_EMAIL})

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [cust_email]
            )
        except Exception as e:
            raise

    def handle_event(self, event):
        """
        From Boutique Ado walkthrough.
        Handle a generic/unknown/unexpected webhook event
        """

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe.

        This method processes a successful payment intent from Stripe,
        extracts necessary information from the event data, and handles
        the creation or verification of a spa booking in the system.

        Args:
            event (dict): The webhook event object from Stripe containing
            information about the payment intent.

        Returns:
            HttpResponse or JsonResponse: Depending on the outcome of
            processing:
                - If the booking is successfully created or verified,
                returns an HttpResponse
                with a success message and status code 200.
                - If an error occurs during booking creation or verification,
                returns an HttpResponse with an error message and status
                code 500.

        Raises:
            None
        """
        intent = event.data.object
        pid = intent.id
        metadata = intent.metadata
        save_info = metadata.get('save_info', 'false').lower() == 'true'
        date_and_time = None
        username = metadata.get('username')
        booking_total = metadata.get('booking_total')
        service_details = json.loads(metadata.get('service_details', '[]'))

        booking_id = uuid.uuid4().hex.upper()
        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)
        billing_details = stripe_charge.billing_details
        booking_total = round(stripe_charge.amount / 100, 2)

        booking_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                booking = SpaBooking.objects.get(
                    customer_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    stripe_pid=pid,
                )
                booking_exists = True
                break
            except SpaBooking.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if booking_exists:
            services = SpaBookingServices.objects.filter(spa_booking=booking)
            self._send_confirmation_email(booking, services)
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    f'SUCCESS: Verified booking already in database'
                ),
                status=200
            )

        booking = None
        try:
            booking = SpaBooking.objects.create(
                customer_name=billing_details.name,
                email=billing_details.email,
                phone_number=billing_details.phone,
                stripe_pid=pid,
                date_and_time=date_and_time,
                booking_total=booking_total,
            )

            for service_id, quantity in metadata.items():
                if service_id.startswith('service_'):
                    service_id = int(service_id.split('_')[1])
                    service = SpaService.objects.get(pk=service_id)
                    date_and_time_str = f"{selected_date} {selected_time}"
                    date_and_time = datetime.strptime(
                        date_and_time_str, "%B %d, %Y %H:%M")
                    date_and_time = make_aware(
                        date_and_time, get_current_timezone())

                    SpaBookingServices.objects.create(
                        spa_booking=booking,
                        spa_service=service,
                        quantity=int(quantity),
                        date_and_time=date_and_time,
                    )

            services = SpaBookingServices.objects.filter(spa_booking=booking)
            self._send_confirmation_email(booking, services)
            return JsonResponse({'success': True}, status=200)

        except Exception as e:
            if booking:
                booking.delete()
            return HttpResponse({'error': str(e)}, status=500)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook
        from Stripe. From Boutique Ado walkthrough.

        This method processes a payment failure webhook
        event from Stripe.

        Args:
            event (dict): The webhook event object from
            Stripe containing information about the payment
            failure.

        Returns:
            HttpResponse: An HttpResponse confirming receipt of
            the webhook event.

        Raises:
            None

        Notes:
            This method is responsible for handling Stripe webhook
            events when a payment intent fails. It logs the event type
            and may perform additional error handling
            or logging as needed.
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',)
