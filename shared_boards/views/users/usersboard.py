from django.shortcuts import render, redirect
from django.contrib import messages
from shared_boards.form.userboardform import userboardForm
from common.models import Transaction, Board , Account
from decimal import Decimal
# Create your views here.

def userboard(request, slug):
    board = Board.objects.get(slug=slug)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            
            # Transaction.objects.create(
            #     typet=typet,
            #     Account=account,
            #     board=board,
            #     user=request.user.username if request.user.is_authenticated else 'anonimo',
            #     status=form.cleaned_data['status'],
            #     date=form.cleaned_data['date'],
            #     amount=amount,
            #     description=form.cleaned_data['description'],
            #     payment_method=form.cleaned_data['payment_method'],
            #     addressee_sender=form.cleaned_data['addressee_sender'],
            # )
            
            messages.success(request, 'The item has been created.')
            return redirect('income:Transaction', slug)
        else:
            messages.error(request, 'Item creation failure.')
            # Redirect or render as appropriate
    else:
        
        transactions = Transaction.objects.filter(board=board)
        form = userboardForm()
    
    return render(request, './boards/userboard.html', {
        'transactions': transactions,
        'form': form,
    })