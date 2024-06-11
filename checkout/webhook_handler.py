from django.http import HttpResponse
from booking.models import SpaBooking, SpaBookingServices
from services.models import SpaService

import logging

import stripe
import json
import time


logger = logging.getLogger(__name__)

class StripeWH_Handler:
    """From Boutique Ado walkthrough. Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )  
        

    def handle_event(self, event):
        """
        From Boutique Ado walkthrough. Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)


    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        logger.info("Handling payment_intent.succeeded webhook: %s", event["id"])


        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info

        logger.debug("Extracted data: pid=%s, cart=%s, save_info=%s", pid, cart, save_info)


        # Fetch the charge using the latest_charge ID
        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)

        # Retrieve billing details and amount from the charge
        billing_details = stripe_charge.billing_details
        booking_total = round(stripe_charge.amount / 100, 2)


        #billing_details = intent.charges.data[0].billing_details
        #booking_total = round(intent.charges.data[0].amount / 100, 2)

        booking_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                booking = SpaBooking.objects.get(
                    customer_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    booking_total=booking_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                booking_exists = True
                break
            except SpaBooking.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if booking_exists:
            self._send_confirmation_email(order)
            logger.info("Verified booking already exists in the database")

            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified booking already in database',
                status=200)

        booking = None
        try:
            booking = SpaBooking.objects.create(
                customer_name=billing_details.name,
                email=billing_details.email,
                phone_number=billing_details.phone,
                original_cart=cart,
                stripe_pid=pid,
            )
            for service_id, service_data in json.loads(cart).items():
                service = SpaService.objects.get(pk=service_id)
                quantity = service_data.get('quantity', 1)
                date_and_time = service_data.get('date_and_time', None)
                spa_booking_service = SpaBookingServices.objects.create(
                    spa_booking=booking,
                    spa_service=service,
                    quantity=quantity,
                    date_and_time=date_and_time,
                )
            logger.info("Booking creation successful. Booking ID: %s", booking.id)
            return JsonResponse({'success': True}, status=200)

        except Exception as e:
            if booking:
                booking.delete()
                logger.error("An error occurred during booking creation: %s", e)
            return HttpResponse({'error': str(e)}, status=500)

        logger.info("Completed handling payment_intent.succeeded webhook: %s", event["id"])
        
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created booking in webhook',
            status=200)


    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)