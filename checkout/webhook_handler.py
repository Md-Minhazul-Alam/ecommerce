from django.http import HttpResponse
import stripe

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic or unknown webhook event
        """
        return HttpResponse(
            content=f'Unhandled event: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        print(f"Payment succeeded for PaymentIntent: {intent.id}")

        # TODO: Mark the related order as paid here
        # Example:
        # order = Order.objects.get(stripe_pid=intent.id)
        # order.payment_status = 'paid'
        # order.save()

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | Payment succeeded: {intent.id}',
            status=200
        )


    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        intent = event.data.object
        print("Payment failed for:", intent.id)
        return HttpResponse(
            content=f'Payment failed: {intent.id}',
            status=200
        )
