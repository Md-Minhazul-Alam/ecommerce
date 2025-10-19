from django.contrib import admin
from .models import Order, OrderLineItem

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number',
        'date',
        'delivery_cost',
        'order_total',
        'grand_total',
    )

    fields = (
        'user_profile',
        'order_number',
        'date',
        'full_name',
        'email',
        'phone_number',
        'country',
        'postcode',
        'town_or_city',
        'street_address1',
        'street_address2',
        'county',
        'delivery_cost',
        'order_total',
        'grand_total',
    )

    list_display = (
        'order_number',
        'full_name',
        'user_profile',
        'date',
        'order_total',
        'delivery_cost',
        'grand_total',
    )

    ordering = ('-date',)

    def save_model(self, request, obj, form, change):
        """Ensure totals are recalculated on save."""
        super().save_model(request, obj, form, change)
        obj.update_total()
