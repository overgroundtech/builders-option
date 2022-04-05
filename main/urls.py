from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('search', views.search, name="search"),
    path('products/<str:product_url>', views.products, name="products"),
    path('categries/<str:category_url>', views.categories, name="categories"),
    # cart urls
    path('cart', views.cart_detail, name="cart"),
    path('cart/add_item/<str:prod_id>/<int:quantity>', views.add_item, name="add-item"),
    path('cart/remove_item/<int:prod_id>/', views.remove_item, name="remove-item"),

    path('checkout', views.checkout, name="checkout")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
