from django.contrib import admin
from .models import HeroSlider

# Register your models here.
class HeroSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'image', 'link')
    search_fields = ('title', 'subtitle')
    list_filter = ('title',)

admin.site.register(HeroSlider, HeroSliderAdmin)