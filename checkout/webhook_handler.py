from django.http import HttpResponse
from checkout.models import Order, OrderLineItem
from product.models import Product
import json
import stripe
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handle generic or unknown webhook event"""
        return HttpResponse(
            content=f'Unhandled event: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe safely"""
        try:
            intent = event.data.object
            pid = intent.id

            # Extract from PaymentIntent metadata (this is where cache_checkout_data stored it)
            metadata = intent.metadata
            bag = getattr(metadata, 'bag', '{}')
            save_info = getattr(metadata, 'save_info', False)
            
            # Get ALL billing info from metadata
            full_name = getattr(metadata, 'full_name', '')
            email = getattr(metadata, 'email', '')
            phone_number = getattr(metadata, 'phone_number', '')
            street_address1 = getattr(metadata, 'street_address1', '')
            street_address2 = getattr(metadata, 'street_address2', '')
            town_or_city = getattr(metadata, 'town_or_city', '')
            postcode = getattr(metadata, 'postcode', '')
            country = getattr(metadata, 'country', '')
            county = getattr(metadata, 'county', '')

            # Get amount from charge
            latest_charge_id = getattr(intent, 'latest_charge', None)
            if latest_charge_id:
                stripe_charge = stripe.Charge.retrieve(latest_charge_id)
                grand_total = round(stripe_charge.amount / 100, 2)
            else:
                grand_total = round(intent.amount / 100, 2)

            # --- Try finding existing order ---
            order_exists = False
            attempt = 1
            order = None

            while attempt <= 5:
                try:
                    order = Order.objects.get(
                        full_name__iexact=full_name,
                        email__iexact=email,
                        phone_number__iexact=phone_number,
                        country__iexact=country,
                        postcode__iexact=postcode,
                        town_or_city__iexact=town_or_city,
                        street_address1__iexact=street_address1,
                        street_address2__iexact=street_address2,
                        county__iexact=county,
                        grand_total=grand_total,
                        original_bag=bag,
                        stripe_pid=pid,
                    )
                    order_exists = True
                    break
                except Order.DoesNotExist:
                    attempt += 1
                    time.sleep(1)

            if order_exists:
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified existing order',
                    status=200
                )

            # --- Create order if not found ---
            order = Order.objects.create(
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                country=country,
                postcode=postcode,
                town_or_city=town_or_city,
                street_address1=street_address1,
                street_address2=street_address2,
                county=county,
                grand_total=grand_total,
                original_bag=bag,
                stripe_pid=pid,
            )

            # --- Create OrderLineItems safely ---
            bag_data = json.loads(bag)
            for item_id, item_data in bag_data.items():
                product = Product.objects.get(id=item_id)

                # If variations exist
                if isinstance(item_data, dict) and 'items_by_variation' in item_data:
                    for variation_key, variation_info in item_data['items_by_variation'].items():
                        quantity = variation_info.get('quantity', 0)
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            product_variation=str(variation_info.get('variations', '')),
                            quantity=quantity,
                            lineitem_total=product.price * quantity
                        )
                # If simple quantity
                elif isinstance(item_data, dict) and 'quantity' in item_data:
                    quantity = item_data.get('quantity', 0)
                    OrderLineItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        lineitem_total=product.price * quantity
                    )
                # If item_data is just an int
                elif isinstance(item_data, int):
                    OrderLineItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item_data,
                        lineitem_total=product.price * item_data
                    )

            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Created order {order.id}',
                status=200
            )

        except Exception as e:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {str(e)}',
                status=500
            )

    def handle_payment_intent_payment_failed(self, event):
        """Handle payment_intent.payment_failed webhook"""
        intent = event.data.object
        print("Payment failed for:", intent.id)
        return HttpResponse(
            content=f'Payment failed: {intent.id}',
            status=200
        )