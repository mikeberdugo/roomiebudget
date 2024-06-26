from django.shortcuts import render
from common.models import Account
from accounts.forms.AccountForm import AccountForm
from django.contrib import messages

## assets and liabilities - posible cambio de nombre y modelo 

def accounts(request ):
    
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario
            name = form.cleaned_data['name']
            balance = form.cleaned_data['balance']
            currency = form.cleaned_data['currency']
            account_type = form.cleaned_data['account_type']
            status = form.cleaned_data['status']
            
            Account.objects.create(
                user =
                name = 
                balance =
                currency = 
                account_type = 
                status = 
            )
            messages.success(request, 'the Item has been created.')
            return redirect('shopping:shoppinglistsviews')
        else:
            messages.error(request, 'Item creation failure.')
            return redirect('shopping:shoppinglistsviews')   
    else :
        accounts = Account.objects.all()
        form = AccountForm()
        
    return render(request, './accounts/accounts.html' , {'accounts':accounts
                                                        ,'form':form 
                                                        })