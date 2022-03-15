from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('products/', views.products, name="products"),
    path('categries/', views.categories, name="categories"),
    path('cart/', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout")
]
