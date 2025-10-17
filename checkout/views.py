from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages

from businessprofile.models import WebsiteSetting
from .forms import OrderForm
from product.models import Category, Product
from checkout.models import Order, OrderLineItem

from .forms import OrderForm
from bag.contexts import bag_contents
from django.conf import settings
import stripe
import json

@require_POST
def cache_checkout_data(request):
    """
    Caches checkout data in Stripe PaymentIntent metadata
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': str(request.user),
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''),
            'phone_number': request.POST.get('phone_number', ''),
            'street_address1': request.POST.get('street_address1', ''),
            'street_address2': request.POST.get('street_address2', ''),
            'town_or_city': request.POST.get('town_or_city', ''),
            'postcode': request.POST.get('postcode', ''),
            'country': request.POST.get('country', ''),
            'county': request.POST.get('county', ''),
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)
    

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Setting 
    setting = WebsiteSetting.objects.first()

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
    stripe_total = round(total * 100)  
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            client_secret = request.POST.get('client_secret')
            if client_secret:
                request.session['checkout_data'] = form_data
                request.session.modified = True
            
            # Save info preference
            request.session['save_info'] = 'save-info' in request.POST

            return redirect(reverse('checkout_success', args=['pending']))
        else:
            messages.error(request, "There was an error with your form. Please double-check your information.")
    else:
        order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, "Stripe public key is missing. Check your environment variables.")

    context = {
        'setting': setting,
        'menuCategories': menuCategories,
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    # Handle successful checkouts
    save_info = request.session.get('save_info')
    
    # If order_number is 'pending', wait for webhook or show temporary message
    if order_number == 'pending':
        setting = WebsiteSetting.objects.first()
        menuCategories = Category.objects.filter(
            is_active=True,
            parent_category__isnull=True
        ).prefetch_related("subcategories")
        
        context = {
            'setting': setting,
            'menuCategories': menuCategories,
            'pending': True,
        }
        return render(request, 'checkout/checkout_success.html', context)
    
    order = get_object_or_404(Order, order_number=order_number)

    messages.success(request, f'Order successfully processed! Your order number is {order_number}. '
                              f'A confirmation email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    # Setting 
    setting = WebsiteSetting.objects.first()

    # Menu categories
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    # Get order line items
    line_items = order.lineitems.select_related('product')

    context = {
        'setting': setting,
        'order': order,
        'line_items': line_items,
        'menuCategories': menuCategories,
    }

    return render(request, 'checkout/checkout_success.html', context)