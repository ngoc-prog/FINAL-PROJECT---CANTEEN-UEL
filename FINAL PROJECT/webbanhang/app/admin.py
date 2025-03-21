from django.contrib import admin
from django.urls import path
from django.db.models import Sum, Count
from django.utils import timezone
from django.template.response import TemplateResponse
from .models import Category, Product, Order, OrderItem, ShippingAddress, Feedback

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_sub', 'sub_category')  
    prepopulated_fields = {'slug': ('name',)}  
    search_fields = ('name',)  
    list_filter = ('is_sub',)  

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'digital', 'get_category_list')  
    search_fields = ('name', 'price')
    list_filter = ('digital', 'category')
    list_per_page = 10  

    def get_category_list(self, obj):
        return ", ".join([c.name for c in obj.category.all()])
    get_category_list.short_description = "Danh mục"
    def get_sales_count(self, obj):
        return OrderItem.objects.filter(product=obj).count()
    get_sales_count.short_description = "Số lượng đã bán"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_order', 'complete', 'transaction_id', 'get_cart_total')
    search_fields = ('customer__username', 'transaction_id')
    list_filter = ('complete', 'date_order')
    ordering = ('-date_order',)
    readonly_fields = ('date_order', 'transaction_id', 'get_cart_total', 'get_cart_items')
    actions = ['mark_as_complete']

    def mark_as_complete(self, request, queryset):
        for order in queryset:
            if not order.complete:
                order.complete_order()
        self.message_user(request, f"{queryset.count()} đơn hàng đã được đánh dấu hoàn thành")
    mark_as_complete.short_description = "Đánh dấu đơn hàng đã hoàn thành"

    def get_cart_total(self, obj):
        return f"{obj.get_cart_total:,.0f} VNĐ"
    get_cart_total.short_description = "Tổng giá trị"
    def save_model(self, request, obj, form, change):
        if 'complete' in form.changed_data and obj.complete:
            if not obj.transaction_id:
                obj.transaction_id = f"TXN-{obj.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            obj.complete_order()
        super().save_model(request, obj, form, change)
    list_display = ('id', 'customer', 'date_order', 'complete', 
                   'transaction_id', 'get_cart_total', 'get_cart_items')
    
    def get_cart_items(self, obj):
        return obj.get_cart_items
    get_cart_items.short_description = "Số lượng sản phẩm"
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order', 'quantity', 'get_total_price')
    search_fields = ('product__name',)
    list_filter = ('order', 'date_added')

    def get_total_price(self, obj):
        return f"{obj.get_total:,.0f} VNĐ"
    get_total_price.short_description = "Thành tiền"

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'address', 'city', 'state', 'phone')
    search_fields = ('customer__username', 'address', 'city')
    list_filter = ('city', 'state', 'date_added')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'comment', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    list_filter = ('rating', 'created_at')
    list_per_page = 10
    ordering = ('-created_at',)
