from .models import Category

def menu_categories(request):
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")
    return {'menuCategories': menuCategories}
