from django.contrib import admin
from .models import Address, Order, OrderItem


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'house', 'street', 'city', 'state', 'zip_code')
    search_fields = ('house', 'street', 'city', 'state', 'zip_code')


class OrderItemInline(admin.TabularInline):
    """
    Defines an inline for the OrderItem model, which allows
    adding and editing OrderItem instances directly from the Order admin page.
    """
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'total_price', 'paid', 'created_at', 'modified_at')
    list_editable = ('total_price', 'paid')
    list_filter = ('user', 'paid', 'created_at', 'modified_at')
    search_fields = ('id', 'user__username', 'address__street', 'address__city', 'address__state', 'address__zip_code')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'item', 'quantity')
    list_editable = ['quantity']
    search_fields = ('order__user__username', 'item__name')
