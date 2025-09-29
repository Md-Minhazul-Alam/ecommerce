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
def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'product/product_detail.html', context)