from django.shortcuts import render
from product.models import Category


# Home Page 
def all_products(request):
    categoryMenu = Category.objects.all()


    context = {
        'categoryMenu': categoryMenu,

    }
    return render(request, "product/products.html", context)

