from django.contrib import admin
from .models import Tag, Brand, Category

# Register Tag
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'tag_slug')
    search_fields = ('tag',)
    list_per_page = 25

admin.site.register(Tag, TagAdmin)

# Register Brand
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand', 'brand_slug')
    search_fields = ('brand',)
    list_per_page = 25

admin.site.register(Brand, BrandAdmin)

# Register Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'category_slug', 'parent_category')
    search_fields = ('category',)
    list_per_page = 25
    
admin.site.register(Category, CategoryAdmin)