from django.shortcuts import render ,redirect
from common.models import Account , Board
from accounts.forms.AccountForm import AccountForm 
from django.contrib import messages

## assets and liabilities - posible cambio de nombre y modelo 

def accounts(request ,slug):
    board = Board.objects.get(slug = slug)

    if request.method == 'POST':
        form = AccountForm(request.POST)
        user = request.user
        if form.is_valid():
            # Procesar los datos del formulario
            name = form.cleaned_data['name']
            balance = form.cleaned_data['balance']
            currency = form.cleaned_data['currency']
            account_type = form.cleaned_data['account_type']
            status = form.cleaned_data['status']
            
            Account.objects.create(
                user = user,
                name = name, 
                balance = balance,
                currency = currency, 
                account_type = account_type, 
                status = status, 
                board = board 
            )
            messages.success(request, 'the Item has been created.')
            return redirect('accounts:accounts',slug)
        else:
            messages.error(request, 'Item creation failure.')
            return redirect('accounts:accounts',slug)   
    else :
        accounts = Account.objects.filter(board = board)
        form = AccountForm()
        
    return render(request, './accounts/accounts.html' , {
                                                        'accounts':accounts
                                                        ,'form':form 
                                                        ,'board':board
                                                        })