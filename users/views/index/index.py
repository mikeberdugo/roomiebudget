from django.shortcuts import render,redirect
from common.models import Board 
from shared_boards.form.boardform import BoardForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

### index login 




@login_required
def index_login(request):
    user = request.user
    boards = Board.objects.filter(creator_user = user)
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            
            data = form.cleaned_data
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
    
    return render(request, './users/index.html', {'boards':boards,
        'form': form, })

