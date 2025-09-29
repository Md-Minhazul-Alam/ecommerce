from django.shortcuts import render, get_object_or_404
from product.models import Category, Product


# Home Page 
def all_products(request):
    categoryMenu = Category.objects.all()

    # Show All Products 
    products = Product.objects.all()


    context = {
        'categoryMenu': categoryMenu,
        'products': products,

    }
    return render(request, "product/products.html", context)

# Product Details
def product_detail(request, product_slug):

    
    categoryMenu = Category.objects.all()
    
    # Product Details
    product = get_object_or_404(Product, product_slug=product_slug)

    context = {
        "product": product,
        "categoryMenu": categoryMenu,
    }
    return render(request, "product/product_details.html", context)