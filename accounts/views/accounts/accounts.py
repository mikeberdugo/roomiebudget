from django.shortcuts import render
from common.models import Account
from accounts.forms.AccountForm import AccountForm




def accounts(request ):
    accounts = Account.objects.all()
    form = AccountForm()
    
    return render(request, './accounts/accounts.html' , {'accounts':accounts
                                                        ,'form':form 
                                                        })