from django.db import models
from main.models import Order

class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    transaction_id = models.CharField(max_length=100)
    merchant_id = models.CharField(max_length=100)
    checkout_id = models.CharField(max_length=100)
    result_desc = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    
    def __str__(self):
        return f'transaction for {order.id}'