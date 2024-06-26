import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler


@require_POST
@csrf_exempt
def webhook(request):
    """
    From Boutique Ado walkthrough.
    Listen for webhooks from Stripe and handle accordingly.

    This view function is designed to receive HTTP POST
    requests containing webhook events from Stripe. It verifies
    the authenticity of the webhook using the secret key configured
    in Django settings. Upon successful verification, it
    constructs the event object and dispatches it to
    the appropriate handler method
    based on the event type.

    Args:
        request (HttpRequest): The HTTP request object
        containing the webhook data.

    Returns:
        HttpResponse: An HTTP response indicating the status
        of processing the webhook
                      event.

    Raises:
        None
    """
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META.get(
        'HTTP_STRIPE_SIGNATURE')
    event = None

    if not sig_header:
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    except Exception as e:
        return HttpResponse(content=str(e), status=400)

    handler = StripeWH_Handler(request)

    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed':
            handler.handle_payment_intent_payment_failed,
    }

    event_type = event['type']
    event_handler = event_map.get(event_type, handler.handle_event)

    response = event_handler(event)
    return response
