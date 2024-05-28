from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'modified_at']
    search_fields = ['user__username']
    list_filter = ['created_at', 'modified_at']
    inlines = [CartItemInline]


admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'item', 'quantity']
    search_fields = ['cart__user__username', 'item__name']
    list_filter = ['cart', 'item']


admin.site.register(CartItem, CartItemAdmin)
