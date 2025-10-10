from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from product.models import Category 

def checkout(request):
    # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('all_products'))

    # Initialize form
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save() 
    else:
        form = OrderForm()

    context = {
        'menuCategories': menuCategories,
        'order_form': form,  
        'stripe_public_key': 'pk_test_51SEo4T0MegBTlRFBITARzKwOGFvT8hbZW1vzFKulla3z3ciWTOMkSs4ZpVN7095qKAz1aefyGy4o88aXm6opl5c100jQOxWUNk',
        'client_secret': 'test client secret',
    }

    return render(request, "checkout/checkout.html", context)
