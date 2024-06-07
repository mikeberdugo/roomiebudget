from django.shortcuts import render
from common.models import Account





def accounts(request,slug):
    accounts = Account.objects.get(board__slug=slug)
    
    
    
    return render(request, './accounts/accounts.html' , {'accounts':accounts})