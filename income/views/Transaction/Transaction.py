from django.shortcuts import render, redirect
from django.contrib import messages
from income.forms.TransactionForm import TransactionForm

# Create your views here.

def Transaction(request):
    form = TransactionForm()
    return render(request, './income/Transaction.html',
                  {'form':form}
                  )