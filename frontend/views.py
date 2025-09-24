from django.shortcuts import render
from product.models import Category

# Create your views here.
def home_page(request):
    categoryMenu = Category.objects.all()

    
    return render(request, "frontend/pages/home.html", {
        'categoryMenu': categoryMenu
    })
