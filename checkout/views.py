from django.shortcuts import render
from .forms import OrderForm
from product.models import Category 

def checkout(request):
    # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

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
