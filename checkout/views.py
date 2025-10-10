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
    }

    return render(request, "checkout/checkout.html", context)
