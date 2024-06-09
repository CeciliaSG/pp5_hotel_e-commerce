from django.http import HttpResponse


class StripeWH_Handler:
    """From Boutique Ado walkthrough. Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request


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

            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)


    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)