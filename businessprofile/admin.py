from django.contrib import admin
from .models import WebsiteSetting

# Register your models here.
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('website_name', 'website_address', 'website_contact_phone', 'website_contact_email')
    search_fields = ('website_name', 'website_contact_email')

    def has_add_permission(self, request):
        return not WebsiteSetting.objects.exists()

admin.site.register(WebsiteSetting, SiteSettingsAdmin)