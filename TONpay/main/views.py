from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from api.models import Pay
from api.models import Wallet
import random
import requests
import base64

def index(request):
    return render(request, 'main/main.html')

@require_GET
def get_info(request):
    a = request.GET.get('merchant')
    b = request.GET.get('id')
    c = request.GET.get('sum')
    return a, b, c

def pay(request):

    check_url = f'/check?check_id={merchant + '-' + id}'

    try:
        wallet = Wallet.objects.filter(merchant=merchant).values('wallet')[0]['wallet']
    except: return HttpResponse('Произошла ошибка!')

    context = {
        'wallet': wallet,
        'sum': sum,
        'comment': comment,
        'check_url': check_url
    }
    return render(request, 'main/pay.html', context)

def create_pay(request):
    merchant, sum = get_info(request)
    comment = str(random.randint(100000, 999999))
    for i in merchant, id, sum:
        if i == None:
            return HttpResponse('Произошла ошибка!')

    payment = Pay(merchant=merchant, sum=sum, comment=comment, status=False)
    payment.save()
    id = Pay.objects.filter(merchant=merchant, sum=sum, comment=comment, status=False).values('id')[0]['id']

    data = {
        'id': id
    }
    return JsonResponse(data)

@require_GET
def check(request):
    check_id = request.GET.get('check_id')

    try:
        merchant, id = check_id.split('-')

        summ = Pay.objects.filter(merchant=merchant, order_id=id).values('sum')[0]['sum']
        status = Pay.objects.filter(merchant=merchant, order_id=id).values('status')[0]['status']
        comment = Pay.objects.filter(merchant=merchant, order_id=id).values('comment')[0]['comment']
        wallet = Wallet.objects.filter(merchant=merchant).values('wallet')[0]['wallet']

        if not status:
            status = pay_checker(wallet, comment, summ)
            Pay.objects.filter(merchant=merchant, order_id=id).update(status=status)

        context = {
            'payment_status': status,
            'sum': summ
        }
    except: return HttpResponse('Произошла ошибка!')

    return render(request, 'main/check.html', context)

@require_GET
def check_info(request):
    try:
        merchant = request.GET.get('merchant')
        id = request.GET.get('id')

        summ = Pay.objects.filter(merchant=merchant, order_id=id).values('sum')[0]['sum']
        status = Pay.objects.filter(merchant=merchant, order_id=id).values('status')[0]['status']
        comment = Pay.objects.filter(merchant=merchant, order_id=id).values('comment')[0]['comment']


        data = {
            'merchant': merchant,
            'order_id': id,
            'amount': summ,
            'Memo/Tag': comment,
            'status': status
        }
    except: return HttpResponse('Произошла ошибка!')
    return JsonResponse(data)

def pay_checker(wallet, comment, sum):
    API_KEY = 'AFHPIL5LVGVZVEQAAAAMUF5IFKODNLTBSWTQFPJ3N7FBCTXTO53SBHSIEXRUKL4K6PM6WWQ'

    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    url = f'https://tonapi.io/v2/blockchain/accounts/{wallet}/transactions?limit=100&sort_order=desc'
    result = requests.get(url, headers=headers)

    if result.status_code == 200:
        transactions = result.json()['transactions']


        tr_count = len(transactions)
        status = False
        for transaction in range(0, tr_count):
            try:
                com = transactions[transaction]['in_msg']['decoded_body']['text']
                success = transactions[transaction]['success']
                nano_sum = transactions[transaction]['in_msg']['value']
                total_sum = int(nano_sum) / 1000000000
                
                if success == True:
                    if com == comment:
                        if str(total_sum) == str(sum):
                            status = True
            except:
                pass
        return status
