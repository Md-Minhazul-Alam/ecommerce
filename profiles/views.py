from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile
from businessprofile.models import WebsiteSetting
from product.models import Category


@login_required
def user_profile(request):
    # Website Settings
    setting = WebsiteSetting.objects.first()

    # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

   

    # Get or create profile for logged-in user
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if created:
        messages.info(request, "Your profile has been created.")

    context = {
        'setting': setting,
        'menuCategories': menuCategories,
        'profile': profile,
    }

    return render(request, "profiles/profile.html", context)
