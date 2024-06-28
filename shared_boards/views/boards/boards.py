from django.shortcuts import render,redirect
from common.models import Board , AstradUser 
from shared_boards.form.boardform import BoardForm
from django.contrib import messages

# Create your views here.


def boards(request):
    user = request.user
    boards = Board.objects.filter(creator_user = user)
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            
            data = form.cleaned_data
            user = AstradUser.objects.get(id=1)
            new_board = Board(
                name=data['name'],
                creator_user= user,
                description=data['description'],
            )
            
            new_board.save()
            
            messages.success(request, 'El tablero ha sido Creado Correctamente ')
            return redirect('boards:boards')
        else :
            messages.success(request, 'Ha ocurrido un error inesperado')
            return redirect('boards:boards')
            
    else:
        form = BoardForm()
    
    return render(request, './boards/board.html' , {
        'boards':boards,
        'form': form,
        
        })