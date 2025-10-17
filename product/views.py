from django.shortcuts import render, get_object_or_404
from businessprofile.models import WebsiteSetting
from product.models import Category, Product
from django.db.models import Q
from itertools import groupby

# Products 
def all_products(request, category_slug=None):
    # Setting 
    setting = WebsiteSetting.objects.first()
    # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    # Search query
    query = request.GET.get("q")
    show_all = request.GET.get("show_all") == "true"

    # Base queryset
    products = Product.objects.all()

    # Category Filter
    category = None
    if category_slug:
        category = get_object_or_404(Category, category_slug=category_slug, is_active=True)
        
        if show_all:
            sub_categories = category.subcategories.filter(is_active=True).values_list('id', flat=True)
            products = products.filter(Q(category=category) | Q(category__in=sub_categories))
        else:
            products = products.filter(category=category)

    # If search query available, filter by search
    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

    # Product Sorting
    sort = request.GET.get("sort")
    direction = request.GET.get("direction", "asc")

    if sort:
        if sort == "price":
            products = products.order_by("price" if direction == "asc" else "-price")
        elif sort == "rating":
            products = products.order_by("rating" if direction == "asc" else "-rating")
        elif sort == "category":
            products = products.order_by(
                "category__category" if direction == "asc" else "-category__category"
            )

    context = {
        "setting": setting,
        "menuCategories": menuCategories,
        "products": products,
        "category": category,
        "query": query,
        "sort": sort,
        "direction": direction,
        "show_all": show_all,
    }
    return render(request, "product/products.html", context)


# Product Details
def product_detail(request, product_slug):
    # Setting 
    setting = WebsiteSetting.objects.first()
    # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    # Product Details
    product = get_object_or_404(Product, product_slug=product_slug)

    # All variations
    variations = product.product_variations.select_related('variation').all()

    # Group Variations
    grouped_variations = {}
    for name, group in groupby(sorted(variations, key=lambda v: v.variation.name), key=lambda v: v.variation.name):
        grouped_variations[name] = list(group)

    context = {
        "setting": setting,
        'menuCategories': menuCategories,
        'product': product,
        'grouped_variations': grouped_variations,
    }
    return render(request, "product/product_details.html", context)