from django.contrib import admin
from .models import Product, Category, Order, OrderItem, BillingAddress, ProductImages

admin.site.site_header = "Builders Option Admin"
admin.site.site_title = "Builders Option Portal"
admin.site.index_title = "Welcome to Builders Option Admin Portal"


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    extra = 1
    max_num = 4


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'in_stock', 'created_on')
    list_filter = ('categories',)
    ordering = ('created_on',)

    # fields = ['name', ('price', 'discount_price'), 'in_stock', 'details', 'description']
    fieldsets = (
        (None, {
            'fields': ('name', ('price', 'discount_price'), ('in_stock',))
        }),(
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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(BillingAddress)
admin.site.register(OrderItem)

