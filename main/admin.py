from django.contrib import admin
from .models import Product, Category, Order, OrderItem, BillingAddress, ProductImages

admin.site.site_header = "Builders Option Admin"
admin.site.site_title = "Builders Option Portal"
admin.site.index_title = "Welcome to Builders Option Admin Portal"

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(BillingAddress)
admin.site.register(OrderItem)
admin.site.register(ProductImages)
