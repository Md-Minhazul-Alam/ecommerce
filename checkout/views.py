from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from product.models import Category 

from .forms import OrderForm
from bag.contexts import bag_contents
from django.conf import settings
import stripe


def checkout(request):
    # Stripe setup
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    # Check if bag has items
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('all_products'))

    # Get totals from bag context
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)  

    # Create Stripe Payment Intent
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # Handle form
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = OrderForm()

    # Warn if public key missing
    if not stripe_public_key:
        messages.warning(request, "Stripe public key is missing. Check your environment variables.")

    context = {
        'menuCategories': menuCategories,
        'order_form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)