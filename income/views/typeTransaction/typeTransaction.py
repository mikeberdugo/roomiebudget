from django.shortcuts import render, redirect
from django.contrib import messages
from income.forms.TransactionForm import TransactionForm
from common.models import Transaction, Board , Category  
from decimal import Decimal

# Create your views here.

def typeTransactions(request, slug):
    board = Board.objects.get(slug=slug)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['Account']
            typet = form.cleaned_data['typet']
            amount = Decimal(form.cleaned_data['amount'])  # Convert to Decimal
            
            if typet == 'ingreso':
                account.balance += abs(amount)
            elif typet == 'egreso':
                account.balance -= abs(amount)
            
            account.save()
            
            Transaction.objects.create(
                typet=typet,
                Account=account,
                board=board,
                user=request.user.username if request.user.is_authenticated else 'anonimo',
                status=form.cleaned_data['status'],
                date=form.cleaned_data['date'],
                amount=amount,
                description=form.cleaned_data['description'],
                payment_method=form.cleaned_data['payment_method'],
                addressee_sender=form.cleaned_data['addressee_sender'],
            )
            messages.success(request, 'The item has been created.')
            return redirect('income:Transaction', slug)
        else:
            messages.error(request, 'Item creation failure.')
            # Redirect or render as appropriate
    else:
        
        category = Category.objects.all()
        form = TransactionForm(slug=slug)
    
    return render(request, './income/typeTransaction.html', {
        'category': category,
        'form': form,
    })