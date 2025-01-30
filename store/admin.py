from django.contrib import admin, messages
from . import models
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode

# Register your models here.

class InvwnroryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)})
        return format_html('<a href={}>{}</a>', url, collection.products_count)

    def get_queryset(elf, request):
        return super().get_queryset(request).annotate(products_count=Count('products'))

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    required_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 10
    list_filter = ['collection', 'last_update', InvwnroryFilter]
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products were successfully updated', messages.SUCCESS)

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user__first_name', 'user__last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    list_per_page = 10
    autocomplete_fields = ['user']
    search_fields = ['user__first_name__startswith', 'user__last_name__startswith']

    def orders_count(self, customer):
        url = reverse('admin:store_order_changelist') + '?' + urlencode({'customer_id': str(customer.id)})
        return format_html('<a href={}>{}</a>', url, customer.orders_count)
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count('order'))

class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']