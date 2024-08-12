from django.shortcuts import render ,redirect
from common.models import Account , Board
from accounts.forms.AccountForm import AccountForm 
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@login_required
def bills(request):
    
    return render(request, './bills/bills.html' , {
                                                        
                                                        })