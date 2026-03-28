from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from businessprofile.models import WebsiteSetting
from product.models import Category, Product, ProductVariation
from django.db.models import Q
from itertools import groupby
from .forms import ReviewForm, ProductForm
from django.forms import inlineformset_factory


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

    # Related Products
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=product.pk)[:4]

    # Review Form
    form = ReviewForm()

    # Save Review
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to submit a review.')
            return redirect('account_login')
        
        # Check if user already reviewed this product
        if product.reviews.filter(user=request.user).exists():
            messages.warning(request, 'You have already reviewed this product.')
            return redirect(request.path + '#reviews')
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect(request.path + '#reviews')
        else:
            messages.error(request, 'Please correct the errors below.')

    # Reviews — after POST so new review shows immediately
    reviews = product.reviews.filter(is_active=True).order_by('-created_at')

    context = {
        "setting": setting,
        'menuCategories': menuCategories,
        'product': product,
        'grouped_variations': grouped_variations,
        'related_products': related_products,
        'form': form,
        'reviews': reviews,
    }
    return render(request, "product/product_details.html", context)

from .models import Review

# Edit Review
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated successfully!')
            return redirect(request.META.get('HTTP_REFERER', '/') + '#reviews')
    messages.error(request, 'Something went wrong.')
    return redirect(request.META.get('HTTP_REFERER', '/') + '#reviews')


# Delete Review
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        product_slug = review.product.product_slug
        review.delete()
        messages.success(request, 'Your review has been deleted successfully!')
        return redirect('product_detail', product_slug=product_slug)
    messages.error(request, 'Something went wrong.')
    return redirect(request.META.get('HTTP_REFERER', '/') + '#reviews')

# Add Product
@login_required
def add_product(request):
    setting = WebsiteSetting.objects.first()
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    VariationFormSet = inlineformset_factory(
        Product,
        ProductVariation,
        fields=('variation', 'stock'),
        extra=1,
        can_delete=True
    )

    form = ProductForm()
    formset = VariationFormSet()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            formset = VariationFormSet(request.POST, instance=product)
            if product.has_variation and formset.is_valid():
                formset.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_detail', product_slug=product.product_slug)
        else:
            messages.error(request, 'Please correct the errors below.')

    context = {
        'setting': setting,
        'menuCategories': menuCategories,
        'form': form,
        'formset': formset,
    }
    return render(request, 'product/add_product.html', context)