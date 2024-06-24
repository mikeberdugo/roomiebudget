from django.shortcuts import render
from common.models import Account





def accounts(request ):
    accounts = Account.objects.all()
    
    
    return render(request, './accounts/accounts.html' , {'accounts':accounts})