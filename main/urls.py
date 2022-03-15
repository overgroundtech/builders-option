from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('products/', views.products, name="products"),
    path('categries/<str:category_url>', views.categories, name="categories"),
    path('cart', views.cart_detail, name="cart"),
    path('checkout', views.checkout, name="checkout")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
