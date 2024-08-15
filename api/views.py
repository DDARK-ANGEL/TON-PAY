from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from .models import Pay
from .models import Wallet
import random
import requests
import base64


def main(request):
    return render(request, 'api/main.html')

def create_pay(request):
    merchant, sum = get_info(request)
    comment = str(random.randint(100000, 999999))
    for i in merchant, sum:
        if i == None:
            return HttpResponse('Произошла ошибка!')
        
    mer = Wallet.objects.filter(merchant=merchant).values('wallet')[0]['wallet']
    if mer == None:
        return HttpResponse('Произошла ошибка!')

    payment = Pay(merchant=merchant, sum=sum, comment=comment, status=False)
    payment.save()
    id = Pay.objects.filter(merchant=merchant, sum=sum, comment=comment).values('id')[0]['id']

    data = {
        'id': id,
    }
    return JsonResponse(data)

@require_GET
def get_info(request):
    a = request.GET.get('merchant')
    b = request.GET.get('sum')
    return a, b
