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

            # Use empty JSON string if metadata.bag does not exist
            bag = getattr(intent.metadata, 'bag', '{}')
            save_info = getattr(intent.metadata, 'save_info', False)

            # Safely get the latest charge
            latest_charge_id = getattr(intent, 'latest_charge', None)
            if latest_charge_id:
                stripe_charge = stripe.Charge.retrieve(latest_charge_id)
                billing_details = stripe_charge.billing_details
                grand_total = round(stripe_charge.amount / 100, 2)
            else:
                billing_details = intent.charges.data[0].billing_details if intent.charges.data else None
                grand_total = round(intent.amount / 100, 2)

            shipping_details = getattr(intent, 'shipping', None)

            # Clean empty fields in shipping
            if shipping_details and shipping_details.address:
                for field, value in shipping_details.address.items():
                    if value == "":
                        shipping_details.address[field] = None

            # Extract email - try multiple sources
            email = None
            if billing_details and hasattr(billing_details, 'email'):
                email = billing_details.email
            if not email and hasattr(intent.metadata, 'email'):
                email = intent.metadata.email
            if not email:
                email = ''  # Fallback to empty string if still not found

            # --- Try finding existing order ---
            order_exists = False
            attempt = 1
            order = None

            while attempt <= 5:
                try:
                    order = Order.objects.get(
                        full_name__iexact=getattr(shipping_details, 'name', ''),
                        email__iexact=email,
                        phone_number__iexact=getattr(shipping_details, 'phone', ''),
                        country__iexact=getattr(shipping_details.address, 'country', '') if shipping_details else '',
                        postcode__iexact=getattr(shipping_details.address, 'postal_code', '') if shipping_details else '',
                        town_or_city__iexact=getattr(shipping_details.address, 'city', '') if shipping_details else '',
                        street_address1__iexact=getattr(shipping_details.address, 'line1', '') if shipping_details else '',
                        street_address2__iexact=getattr(shipping_details.address, 'line2', '') if shipping_details else '',
                        county__iexact=getattr(shipping_details.address, 'state', '') if shipping_details else '',
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
                full_name=getattr(shipping_details, 'name', ''),
                email=email,
                phone_number=getattr(shipping_details, 'phone', ''),
                country=getattr(shipping_details.address, 'country', '') if shipping_details else '',
                postcode=getattr(shipping_details.address, 'postal_code', '') if shipping_details else '',
                town_or_city=getattr(shipping_details.address, 'city', '') if shipping_details else '',
                street_address1=getattr(shipping_details.address, 'line1', '') if shipping_details else '',
                street_address2=getattr(shipping_details.address, 'line2', '') if shipping_details else '',
                county=getattr(shipping_details.address, 'state', '') if shipping_details else '',
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
