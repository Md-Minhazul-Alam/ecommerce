from django.shortcuts import render, get_object_or_404
from product.models import Category, Product


# Home Page 
def all_products(request):

    # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")
    




    # Show All Products 
    products = Product.objects.all()


    context = {

        'products': products,

    }
    return render(request, "product/products.html", context)


def category_products(request):

    # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    # Show All Products 
    products = Product.objects.all()

    context = {
        'menuCategories': menuCategories,
        'products': products,

    }
    return render(request, "product/products.html", context)

# Product Details
def product_detail(request, product_slug):

    
    # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")
    
    # Product Details
    product = get_object_or_404(Product, product_slug=product_slug)

    context = {
        'menuCategories': menuCategories,
        "product": product,
    }
    return render(request, "product/product_details.html", context)