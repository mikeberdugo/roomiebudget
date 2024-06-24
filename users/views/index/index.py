from django.shortcuts import render
from accounts.forms.AccountForm import AccountForm
from income.forms.TransactionForm import TransactionForm
# Create your views here.

### index login 

def index_login(request):
    form = TransactionForm()
    return render(request, './users/index.html', {'form':form} )
