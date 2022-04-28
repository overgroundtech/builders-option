import requests
from django.contrib.auth import get_user_model


def stk_push(order, billing_address):
    link = "https://tinypesa.com/api/v1/express/initialize"
    auth_key = '2ed7Ve8gQKn'
    
    def verify_phone(phone):
        if phone[0] == '0':
            phone = '254' + phone[0:]
        elif phone[0] == '+':
            phone = phone[0:]
        return phone

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "ApiKey": auth_key
    }

    data = {
        'amount': order.total_price,
        'msisdn': verify_phone(billing_address.phone),
        'account_no': billing_address.phone
    }
    try:
        res = requests.post(link, headers=headers, data=data)
    except requests.exceptions.RequestException as e:
        raise f'{e}'
    
    if res.json()['success'] == True:
        return True
    return False
