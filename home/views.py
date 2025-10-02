from django.shortcuts import render
from product.models import Category, Product
from themeOption.models import HeroSlider
import random

# Home Page 
def home_page(request):
    # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    # Category List
    categoryList = Category.objects.all()

    # Sliders
    sliders = HeroSlider.objects.all()

    # Featured products
    featured_products = list(Product.objects.filter(is_featured=True, is_active=True))
    random.shuffle(featured_products)
    featured_products = featured_products[:8]

    context = {
        'menuCategories': menuCategories,
        'categoryList': categoryList,
        'sliders': sliders,
        'featured_products': featured_products,
    }
    return render(request, "home/index.html", context)