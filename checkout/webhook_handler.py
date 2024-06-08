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