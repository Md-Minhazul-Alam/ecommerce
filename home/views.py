from django.shortcuts import render
from product.models import Category
from themeOption.models import HeroSlider

# Create your views here.
def home_page(request):
    categoryMenu = Category.objects.all()
    sliders = HeroSlider.objects.all()

    return render(request, "home/index.html", {
        'categoryMenu': categoryMenu,
        'sliders': sliders,
    })