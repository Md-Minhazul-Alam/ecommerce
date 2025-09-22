from django.contrib import admin
from .models import Tag, Brand

# Register Tag
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'tag_slug')
    search_fields = ('tag',)

admin.site.register(Tag, TagAdmin)

# Register Brand
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand', 'brand_slug')
    search_fields = ('brand',)

admin.site.register(Brand, BrandAdmin)