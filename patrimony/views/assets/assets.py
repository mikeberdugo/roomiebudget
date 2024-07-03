from django.shortcuts import render,redirect
from common.models import Board , AstradUser , Patrimony
from django.contrib import messages
from patrimony.form.assetsform import assetsform


# Create your views here.


def assets(request,slug):
    board = Board.objects.get(slug = slug)

    if request.method == 'POST':
        form = assetsform(request.POST)
        user = request.user
        if form.is_valid():
            # Procesar los datos del formulario
            name = form.cleaned_data['name']
            balance = form.cleaned_data['balance']
            currency = form.cleaned_data['currency']
            patrimony_type = form.cleaned_data['patrimony_type']
            status = form.cleaned_data['status']
            
            Patrimony.objects.create(
                user = user,
                name = name, 
                balance = balance,
                currency = currency, 
                patrimony_type = patrimony_type, 
                status = status, 
                board = board ,
                type_dos = 1,
            )
            
            messages.success(request, 'the Account has been created.')
            return redirect('patrimony:assets',slug)
        else:
            messages.error(request, 'Account creation failure.')
            return redirect('patrimony:assets',slug)   
    else :
        asserts = Patrimony.objects.filter(board = board ,type_dos=1 )
        form = assetsform()
    return render(request, './patrimony/patrimony.html' , {
        'form': form,
        'asserts':asserts,
        })