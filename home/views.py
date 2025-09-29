from django.shortcuts import render
from product.models import Category, Product
from themeOption.models import HeroSlider
import random

# Home Page 
def home_page(request):
    categoryMenu = Category.objects.all()
    sliders = HeroSlider.objects.all()

    # Featured products randomly
    featured_products = list(Product.objects.filter(is_featured=True, is_active=True))
    random.shuffle(featured_products)
    featured_products = featured_products[:8]  

    context = {
        'categoryMenu': categoryMenu,
        'sliders': sliders,
        'featured_products': featured_products,
    }
    return render(request, "home/index.html", context)

