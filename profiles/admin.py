from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'country', 'created_at')
    search_fields = ('user__username', 'phone', 'city', 'country')
    list_filter = ('country', 'created_at')
    ordering = ('-created_at',)
