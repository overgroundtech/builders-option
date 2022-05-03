from django.db import models
from django.contrib.auth import get_user_model
from main.models import Order


class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    transaction_id = models.CharField(max_length=100)
    merchant_id = models.CharField(max_length=100)
    checkout_id = models.CharField(max_length=100)
    result_desc = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    
    def __str__(self):
        return f'transaction for {self.order.id}'


"""https://19e8-102-68-76-235.ngrok.io/pay

'{
    "Body": {
        "stkCallback": {
            "MerchantRequestID": "26773-830618-1",
            "CheckoutRequestID": "ws_CO_21042021114416028704",
            "ResultCode": 0,
            "ResultDesc": "The service request is processed successfully.",
            "CallbackMetadata": {
                "Item": [
                    {
                        "Name": "Amount",
                        "Value": 1
                    },
                    {
                        "Name": "MpesaReceiptNumber",
                        "Value": "PDL72WRAVZ"
                    },
                    {
                        "Name": "TransactionDate",
                        "Value": 20210421114425
                    },
                    {
                        "Name": "PhoneNumber",
                        "Value": 254718942538
                    }
                ]
            },
            "TinyPesaID": "c002f860-a27d-11eb-a7f4-c141263d7c15",
            "ExternalReference": "customacct",
            "Amount": 1,
            "Msisdn": "254718942538"
        }
    }
}'

"""