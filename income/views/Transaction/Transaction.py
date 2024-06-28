from django.shortcuts import render, redirect
from django.contrib import messages
from income.forms.TransactionForm import TransactionForm
from common.models import Transaction, Board , Account
# Create your views here.

def Transactions(request,slug):
    board = Board.objects.get(slug = slug)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        user = request.user
        if form.is_valid():
            # Procesar los datos del formulario
            account = form.cleaned_data['Account']
            
            labels = form.cleaned_data['labels']
            
            Transaction.objects.create(
                typet=form.cleaned_data['typet'],
                Account=account,
                board=board,  
                user=request.user.username if request.user.is_authenticated else 'anonimo',
                status=form.cleaned_data['status'],
                date=form.cleaned_data['date'],
                amount=form.cleaned_data['amount'],
                description=form.cleaned_data['description'],
                payment_method=form.cleaned_data['payment_method'],
                addressee_sender=form.cleaned_data['addressee_sender'],
            )
            messages.success(request, 'the Item has been created.')
            return redirect('income:Transaction',slug)
        else:
            messages.error(request, 'Item creation failure.')
            return redirect('income:Transaction',slug)   
    else :
        
        transactions = Transaction.objects.filter(board = board)
        form = TransactionForm(slug = slug) 
    return render(request, './income/Transaction.html',
                    {   'transactions':transactions,
                        'form':form
                        
                    })
                    