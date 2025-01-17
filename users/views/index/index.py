from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

### index login 




# @login_required
def index_login(request):
    
    return render(request, './users/index.html')

