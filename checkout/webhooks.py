from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler

import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from checkout.webhook_handler import StripeWH_Handler
import stripe
import logging

logger = logging.getLogger(__name__)

@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', None)
    event = None

    logger.debug("Received webhook: %s", payload)

    if not sig_header:
        logger.error("Missing Stripe signature header.")
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        logger.error("Invalid payload: %s", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error("Invalid signature: %s", e)
        return HttpResponse(status=400)
    except Exception as e:
        logger.error("Error constructing event: %s", e)
        return HttpResponse(content=str(e), status=400)

    logger.debug("Event constructed successfully: %s", event)

    handler = StripeWH_Handler(request)

    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    event_type = event['type']
    event_handler = event_map.get(event_type, handler.handle_event)

    logger.debug("Handling event type: %s", event_type)

    response = event_handler(event)
    logger.debug("Response from handler: %s", response)
    return response
