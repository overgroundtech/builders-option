import json
import time

from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.contrib.messages import info, error
from cart.cart import Cart
from main.models import Order
from .models import Transaction


@csrf_exempt
def callback(request):
    user = request.user
    order = Order.objects.filter(customer_id=user.id).first()
    data = json.loads(request.body)
    print(data)
    stk_results = data["Body"]["stkCallback"]
    if int(stk_results["ResultCode"]) == 0:
        error(request, stk_results["RequestDesc"])
        return redirect('checkout')
    else:
        print('name')
    return HttpResponse('hello')
