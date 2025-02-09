from django.contrib import admin

from order.models import OrderItem, Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('phone', 'address', 'town', 'payment_date', 'payment_method', 'created_date', 'shipped_date', 'delivered_date', 'cancelled_date')

    list_display = ('id', 'user', 'status', 'total_price', 'phone', 'address', 'town', 'created_date', 'receipt_number')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)