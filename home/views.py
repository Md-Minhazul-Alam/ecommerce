from django.shortcuts import render
from product.models import Category
from themeOption.models import HeroSlider

# Home Page 
def home_page(request):
    categoryMenu = Category.objects.all()
    sliders = HeroSlider.objects.all()

    context = {
        'categoryMenu': categoryMenu,
        'sliders': sliders,
    }
    return render(request, "home/index.html", context)

