import json
import logging
import time
from datetime import datetime

import stripe

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.utils.timezone import make_aware, get_current_timezone

from booking.models import SpaBooking, SpaBookingServices
from services.models import SpaService, TimeSlot




logger = logging.getLogger(__name__)

class StripeWH_Handler:
    """From Boutique Ado walkthrough. Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request


    def _send_confirmation_email(self, spa_booking):
        """Send the user a confirmation email."""

        cust_email = None
        try:
            cust_email = spa_booking.email
            subject = render_to_string(
                'checkout/confirmation_emails/confirmation_email_subject.txt',
                {'booking': spa_booking})
            body = render_to_string(
                'checkout/confirmation_emails/confirmation_email_body.txt',
                {'spa_booking': spa_booking, 'contact_email': settings.DEFAULT_FROM_EMAIL})
            
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [cust_email]
            )
            logger.info("Confirmation email sent successfully to %s", cust_email)
        except Exception as e:
            logger.error("Failed to send confirmation email to %s: %s", cust_email, str(e))
            raise


    def handle_event(self, event):
        """
        From Boutique Ado walkthrough. Handle a generic/unknown/unexpected webhook event
        """

        logger.info('Webhook received')
        try:
            payload = request.body
            event = None

            try:
                event = json.loads(payload)
                logger.info(f'Webhook event: {event}')
            except ValueError as e:
                logger.error(f'Webhook error while parsing payload: {e}')
                return HttpResponse(status=400)

            if event['type'] == 'payment_intent.succeeded':
                handle_payment_intent_succeeded(event)
                return HttpResponse(status=200)
            else:
                logger.warning(f'Unhandled event type {event["type"]}')
                return HttpResponse(status=200)

        except Exception as e:
            logger.error(f'Error handling webhook: {e}', exc_info=True)
            return HttpResponse(status=500)

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )


    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        #logger.info("Handling payment_intent.succeeded webhook: %s", event["id"])


        intent = event.data.object
        pid = intent.id
        metadata = intent.metadata
        cart = json.loads(metadata.cart)
        save_info = metadata.get('save_info', 'false').lower() == 'true'

        date_and_time = None

        for unique_key, service_data in cart.items():

            try:    
                service_id, selected_date, selected_time_slot_id = unique_key.split('_')
                time_slot = TimeSlot.objects.get(pk=selected_time_slot_id)
                selected_time = time_slot.time.strftime("%H:%M")
                date_and_time_str = f"{selected_date} {selected_time}"
                date_and_time = datetime.strptime(date_and_time_str, "%B %d, %Y %H:%M")
                date_and_time = make_aware(date_and_time, get_current_timezone())
                logger.debug(f"selected_date: {selected_date}, selected_time: {selected_time}")
                logger.debug(f"date_and_time_str: {date_and_time_str}, date_and_time: {date_and_time}")

                break
            except Exception as e:
                logger.error("Error processing cart item %s: %s", unique_key, e)
                pass

        if not date_and_time:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: Failed to set date_and_time from cart',
                status=500
            )

        # Fetch the charge using the latest_charge ID
        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)

        # Retrieve billing details and amount from the charge
        billing_details = stripe_charge.billing_details
        booking_total = round(stripe_charge.amount / 100, 2)
        cart_json = json.dumps(cart)

        booking_exists = False
        attempt = 1
        print('billing_details.name', billing_details.name)
        print('billing_details.email', billing_details.email)
        print('billing_details.phone', billing_details.phone)
        print('cart_json', cart_json)
        print('pid', pid)
        while attempt <= 5:
            try:
                booking = SpaBooking.objects.get(
                    customer_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    #booking_total=booking_total,
                    original_cart=cart_json,
                    stripe_pid=pid,
                )
                booking_exists = True
                break
            except SpaBooking.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if booking_exists:
            self._send_confirmation_email(booking)
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
                original_cart=cart_json,                    
                stripe_pid=pid,
                date_and_time=date_and_time,
            )
            for service_id, service_data in cart.items():
                service_id = int(unique_key.split('_')[0])
                service = SpaService.objects.get(pk=service_id)
                quantity = service_data.get('quantity', 1)
                #date_and_time = service_data.get('date_and_time', None)
                date_and_time_str = f"{selected_date} {selected_time}"
                date_and_time = datetime.strptime(date_and_time_str, "%B %d, %Y %H:%M")
                date_and_time = make_aware(date_and_time, get_current_timezone())


                if date_and_time is None:
                    logger.warning("No date_and_time found in service_data for service ID: %s", service_id)

                spa_booking_service = SpaBookingServices.objects.create(
                    spa_booking=booking,
                    spa_service=service,
                    quantity=quantity,
                    date_and_time=date_and_time,
                )
            logger.info("Booking creation successful. Booking ID: %s", booking.id)
            return JsonResponse({'success': True}, status=200)
            logger.debug("Extracted data_3: pid=%s, cart=%s, save_info=%s", pid, cart, save_info)

        except Exception as e:
            logger.error(f'An error occurred during booking creation: {e}')
            logger.error('Data used for booking creation: %s', {e})
            if booking:
                booking.delete()
                logger.error("An error occurred during booking creation_2: %s", e)
            return HttpResponse({'error': str(e)}, status=500)

        logger.info("Completed handling payment_intent.succeeded webhook: %s", event["id"])

        self._send_confirmation_email(booking)
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