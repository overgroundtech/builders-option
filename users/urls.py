from django.urls import path
from . import views

urlpatterns = [
    path('sign-in', views.sign_in, name="sign-in"),
    path('sign-up', views.sign_up, name="sign-up"),
    path('dashboard', views.dashboard, name='dashboard'),
    path('edit-billing-address', views.edit_billing_address, name='edit-billing-address'),
    path('edit-account-details', views.edit_account, name='edit-account-details'),
    path('sign-out', views.sign_out, name="sign-out"),
]
