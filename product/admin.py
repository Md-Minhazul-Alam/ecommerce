from django.contrib import admin
from django.utils.html import mark_safe
from .models import Tag, Brand, Category, Variation, Product, ProductVariation

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

# Register Variation
class VariationAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'variation_slug')
    search_fields = ('name', 'value', 'variation_slug')
    list_per_page = 25

admin.site.register(Variation, VariationAdmin)

# Register Product & Variation Inline
class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1  
    autocomplete_fields = ['variation']  

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'get_thumbnail_preview', 'product_slug', 'brand', 'category')
    search_fields = ('product_name', 'product_slug')
    list_filter = ('brand', 'category', 'is_active', 'is_featured')
    filter_horizontal = ('tags',)
    inlines = [ProductVariationInline] 

    # Show image preview in list view and edit form
    def get_thumbnail_preview(self, obj):
        if obj.thumbnail:
            return mark_safe(f'<img src="{obj.thumbnail.url}" width="60" height="60" style="object-fit:cover; border-radius:4px;" />')
        return "—"
    get_thumbnail_preview.short_description = "Thumbnail"

    # Make the preview appear in the edit form
    readonly_fields = ('get_thumbnail_preview',)

admin.site.register(Product, ProductAdmin)

# Register Product Variation Admin
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation', 'stock', 'get_price')
    list_filter = ('product', 'variation')

    def get_price(self, obj):
        return obj.product.price
    get_price.short_description = 'Base Price'

admin.site.register(ProductVariation, ProductVariationAdmin)
