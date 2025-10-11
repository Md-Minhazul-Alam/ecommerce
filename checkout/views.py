from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import OrderForm
from product.models import Category, Product
from checkout.models import Order, OrderLineItem

from .forms import OrderForm
from bag.contexts import bag_contents
from django.conf import settings
import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Menu categories for header
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('all_products'))

    # Calculate totals from bag
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)  # Stripe expects cents
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()

            # OrderLineItem for each item in bag
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(pk=item_id)

                    # Has variations
                    if 'items_by_variation' in item_data:
                        for variation_key, variation_info in item_data['items_by_variation'].items():
                            quantity = variation_info['quantity']
                            OrderLineItem.objects.create(
                                order=order,
                                product=product,
                                product_variation=str(variation_info['variations']),
                                quantity=quantity,
                                lineitem_total=product.price * quantity
                            )
                    # No variations
                    else:
                        quantity = item_data['quantity']
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            lineitem_total=product.price * quantity
                        )

                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!"
                    ))
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Recalculate totals
            order.update_total()

            # Save info 
            request.session['save_info'] = 'save-info' in request.POST

            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, "There was an error with your form. Please double-check your information.")
    else:
        form = OrderForm()
        if not stripe_public_key:
            messages.warning(request, "Stripe public key is missing. Check your environment variables.")

    context = {
        'menuCategories': menuCategories,
        'order_form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    # Handle successful checkouts

    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    messages.success(request, f'Order successfully processed! Your order number is {order_number}. '
                              f'A confirmation email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    # Menu categories
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    # Get order line items
    line_items = order.lineitems.select_related('product')

    context = {
        'order': order,
        'line_items': line_items,
        'menuCategories': menuCategories,
    }

    return render(request, 'checkout/checkout_success.html', context)
