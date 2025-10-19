from .models import Category
import random

def menu_categories(request):
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")
    return {'menuCategories': menuCategories}


def footer_categories(request):
    categories = list(
        Category.objects.filter(is_active=True)
    )
    random.shuffle(categories)
    return {'footerCategories': categories[:8]}
