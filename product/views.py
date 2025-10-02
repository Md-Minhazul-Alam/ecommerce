from django.shortcuts import render, get_object_or_404
from product.models import Category, Product
from django.db.models import Q

# Home Page 
def all_products(request):
    # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    # Search query
    query = request.GET.get("q")

    if query:
        products = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
    else:
        products = Product.objects.all()

    context = {
        "menuCategories": menuCategories,
        "products": products,
        "query": query,
    }
    return render(request, "product/products.html", context)


def category_products(request, category_slug):
    # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    # Category object
    category = get_object_or_404(Category, category_slug=category_slug, is_active=True)

    # Filter products for this category
    products = Product.objects.filter(category=category)

    context = {
        "menuCategories": menuCategories,
        "category": category,
        "products": products,
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