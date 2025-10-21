from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from businessprofile.models import WebsiteSetting
from product.models import Category, Product
from checkout.models import Order, OrderLineItem
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from .forms import OrderForm
from bag.contexts import bag_contents

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
        return HttpResponse(content=str(e), status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Settings 
    setting = WebsiteSetting.objects.first()

    # Menu categories
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    # Get bag from session
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('all_products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key

    # Create Stripe PaymentIntent
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if request.method == 'POST':
        # Collect form data
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
            order = order_form.save(commit=False)

            # Attach Stripe PaymentIntent ID
            client_secret = request.POST.get('client_secret')
            if client_secret:
                pid = client_secret.split('_secret')[0]
                order.stripe_pid = pid

            order.original_bag = json.dumps(bag)
            order.save()

            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(pk=item_id)

                    if 'items_by_variation' in item_data:
                        for variation_key, variation_info in item_data['items_by_variation'].items():
                            quantity = variation_info['quantity']

                            # Extract variation(s)
                            variations = variation_info.get('variations', {})
                            if isinstance(variations, dict):
                                # Join multiple variations into readable text
                                variation_text = ", ".join([f"{v}" for v in variations.values()])
                            else:
                                variation_text = str(variations)

                            # Save readable variation (e.g. "64 gb")
                            OrderLineItem.objects.create(
                                order=order,
                                product=product,
                                product_variation=variation_text,
                                quantity=quantity,
                                lineitem_total=product.price * quantity
                            )
                    else:
                        quantity = item_data.get('quantity', 1)
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

            # Update order total
            order.update_total()
            request.session['save_info'] = 'save-info' in request.POST

            # Send confirmation email
            _send_confirmation_email(order)

            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, "There was an error with your form. Please double-check your information.")

    else:
        # Pre-fill form if user is logged in
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.phone,
                    'country': profile.country,
                    'postcode': profile.postal_code,
                    'town_or_city': profile.city,
                    'street_address1': profile.address_line1,
                    'street_address2': profile.address_line2,
                    'county': profile.state,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
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
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    # Default line_items in case order exists but has no items
    line_items = order.lineitems.select_related('product') if order else []

    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)

        order.user_profile = profile
        order.save()

        # Update user profile if save_info was checked
        if save_info:
            profile_data = {
                'phone': order.phone_number,
                'country': order.country,
                'postal_code': order.postcode,
                'city': order.town_or_city,
                'address_line1': order.street_address1,
                'address_line2': order.street_address2,
                'state': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(
        request,
        f'Order successfully processed! Your order number is {order_number}. '
        f'A confirmation email will be sent to {order.email}.'
    )

    # Clear shopping bag from session
    if 'bag' in request.session:
        del request.session['bag']

    # Website settings and menus
    setting = WebsiteSetting.objects.first()
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related('subcategories')

    context = {
        'setting': setting,
        'order': order,
        'line_items': line_items,
        'menuCategories': menuCategories,
    }

    return render(request, 'checkout/checkout_success.html', context)


def _send_confirmation_email(order):
    """
    Send a confirmation email to the user
    """
    cust_email = order.email
    subject = render_to_string(
        'checkout/confirmation_emails/confirmation_email_subject.txt',
        {'order': order}
    )
    body = render_to_string(
        'checkout/confirmation_emails/confirmation_email_body.txt',
        {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
    )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )
