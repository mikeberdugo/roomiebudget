from django.shortcuts import render , redirect 
from shared_boards.form.boardform import BoardForm
from django.shortcuts import render,redirect
from django.contrib import messages

## modelo : 
from common.models import Board




# Create your views here.


def createboard(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            
            data = form.cleaned_data
            
            new_board = Board(
                name=data['name'],
                creator_user= None,
                description=data['description'],
                categories= data['categories'] ,
            )
            
            new_board.save()
            
            messages.success(request, 'El tablero ha sido Creado Correctamente ')
            return redirect('admin:companies')
        else :
            messages.success(request, 'Ha ocurrido un error inesperado')
            
    else:
        form = BoardForm()
        
    return render(request, './boards/createboard.html',
                { 'form': form,
                    
                })