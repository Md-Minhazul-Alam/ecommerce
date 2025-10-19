from django.contrib import admin
from .models import WebsiteSetting
from .models import QuickLink, LegalLink

# Register your models here.
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('website_name', 'website_address', 'website_contact_phone', 'website_contact_email')
    search_fields = ('website_name', 'website_contact_email')

    def has_add_permission(self, request):
        return not WebsiteSetting.objects.exists()

admin.site.register(WebsiteSetting, SiteSettingsAdmin)

# QuickLink Admin
@admin.register(QuickLink)
class QuickLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug')
    list_filter = ('is_active',)
    ordering = ('title',)


# LegalLink Admin
@admin.register(LegalLink)
class LegalLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug')
    list_filter = ('is_active',)
    ordering = ('title',)