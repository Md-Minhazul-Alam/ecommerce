from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from product.models import Product

def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)

        # Product has variations
        if 'items_by_variation' in item_data:
            for variation_key, variation_info in item_data['items_by_variation'].items():
                quantity = variation_info['quantity']
                item_total = quantity * product.price
                total += item_total
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'variations': variation_info['variations'],
                    'variation_key': variation_key,
                    'item_total': item_total,
                })

        # Product without variations
        else:
            quantity = item_data['quantity']
            item_total = quantity * product.price
            total += item_total
            product_count += quantity
            bag_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': product,
                'variations': None,
                'variation_key': None,
                'item_total': item_total,
            })

    # Delivery
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = Decimal(0)
        free_delivery_delta = Decimal(0)
    
    grand_total = total + delivery

    return {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }
