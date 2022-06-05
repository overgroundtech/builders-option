from django.contrib import admin
from django_summernote.models import Attachment
from .models import Product, Category, Order, OrderItem, BillingAddress, ProductImages
from django_summernote.admin import SummernoteModelAdmin

admin.site.site_header = "Builders Option Admin"
admin.site.site_title = "Builders Option Portal"
admin.site.index_title = "Welcome to Builders Option Admin Portal"

admin.site.unregister(Attachment)


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    extra = 0
    min_num = 1
    max_num = 4


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    list_display = ('name', 'price', 'on_deals', 'in_stock', 'created_on')
    list_filter = ('categories',)
    ordering = ('created_on',)
    summernote_fields = '__all__'
    fieldsets = (
        (None, {
            'fields': ('name', ('price', 'discount_price'), ('in_stock', 'on_deals'))
        }), (
          "Select Product Category", {
              "fields": ('categories',)
          }
        ),
        ("Details and Description", {
            'fields': ('details', 'description')
        })
    )
    inlines = [ProductImagesAdmin]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    fieldsets = (
        ("Name", {
           "fields": ("name",)
        }),
        (
            "Image", {
                "fields": ("image",)
            }
        )
    )


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'unit_price', 'total_price')
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('made_on', 'customer', 'paid', 'payment', 'status',)
    ordering = ('-made_on',)
    list_filter = ('paid', 'status')
    inlines = [OrderItemAdmin]
    readonly_fields = ('made_on', 'customer', 'paid', 'payment', 'billing_address', 'order_id', 'notes', 'total_price')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True


@admin.register(BillingAddress)
class BillingAddress(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'lastname', 'county', 'phone', 'email')

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False