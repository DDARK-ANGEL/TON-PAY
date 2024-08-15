from django.shortcuts import render
from .models import Users
from .forms import UsersForm

def merchants_home(request):
    return render(request, 'merchants/main.html')

def login(request):
    logins = Users.objects.values_list('name', flat=True)
    return render(request, 'merchants/login.html')

def register(request):
    form = UsersForm()

    data = {
        'form': form
    }

    return render(request, 'merchants/register.html', data)
