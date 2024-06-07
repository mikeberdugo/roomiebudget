from django.shortcuts import render
from common.models import Board , AstradUser 
from shared_boards.form.boardform import BoardForm


# Create your views here.


def boards(request):
    boards = Board.objects.all()
    
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
            
        else :
            messages.success(request, 'Ha ocurrido un error inesperado')
            
    else:
        form = BoardForm()
    
    return render(request, './boards/board.html' , {
        'boards':boards,
        'form': form,
        
        })