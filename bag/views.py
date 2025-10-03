from django.shortcuts import render
from product.models import Category

# Create your views here.
def view_bag(request):
   # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    

    context = {
        'menuCategories': menuCategories,
    }

    return render(request, "bag/bag.html", context)
