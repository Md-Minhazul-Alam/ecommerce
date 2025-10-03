from django.conf import settings
from decimal import Decimal
from django.shortcuts import get_object_or_404


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0




    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)

    context = {}

    return context