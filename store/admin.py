from django.contrib import admin
from .models import Category, Product, Order, OrderItem
# Register your models here.

# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(Order)
# admin.site.register(OrderItem)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    # prepopulated_fields = {"slug": ("name",)}
    ordering = ("title",)
    search_fields = ("title",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "price", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    list_editable = ("price",)
    # prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description")
    ordering = ("title",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "created_at", "uid", "payment_method", "is_paid", "phone_number", )
    ordering = ("-created_at",)
    search_fields = ("payment_number", "user__username", "status", "created_at", "quan", "total_price", "payment_method", "uid")
    list_filter = ("created_at", "status")
    readonly_fields = ['created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "order", "price", "quantity", "created_at", "updated_at")
    ordering = ("-created_at",)
    search_fields = ("product__title", "order__uid", "price", "quantity", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ['created_at', 'updated_at']