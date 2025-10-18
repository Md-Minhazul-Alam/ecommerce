from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm
from businessprofile.models import WebsiteSetting
from product.models import Category
from checkout.models import Order


@login_required
def profile(request):
    # Website Settings
    setting = WebsiteSetting.objects.first()

    # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    # Get or create profile for logged-in user
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Handle form submission
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserProfileForm(instance=profile)

    # Get order history based on user's email
    orders = Order.objects.filter(email=request.user.email).order_by('-date')

    context = {
        'setting': setting,
        'menuCategories': menuCategories,
        'form': form,
        'orders': orders,
    }

    return render(request, "profiles/profile.html", context)


@login_required
def order_history(request, order_number):
    """
    Display a past order confirmation page for the logged-in user.
    """
    # Get the order or 404
    order = get_object_or_404(Order, order_number=order_number, email=request.user.email)

    # Show message
    messages.info(
        request,
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    )

    return render(
        request,
        'checkout/checkout_success.html',
        {
            'order': order,
            'from_profile': True,
        }
    )