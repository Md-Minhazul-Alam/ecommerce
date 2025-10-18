from django.shortcuts import render, redirect
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
