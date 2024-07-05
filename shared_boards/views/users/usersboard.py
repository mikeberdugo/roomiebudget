from django.shortcuts import render, redirect
from django.contrib import messages
from shared_boards.form.userboardform import userboardForm
from common.models import Transaction, Board , Account , AstradUser , Permit
from decimal import Decimal
# Create your views here.

def userboard(request, slug):
    board = Board.objects.get(slug=slug)
    if request.method == 'POST':
        form = userboardForm(request.POST)
        if form.is_valid():
            
            email_or_id = form.cleaned_data['email_or_id']
            
            if '@' in email_or_id:
                print('correo')
                nuevo_usuario = AstradUser.objects.get(email=email_or_id)
                board.linked_users.add(nuevo_usuario)
                board.save()
                messages.success(request, 'The item has been created. 1')
                return redirect('boards:userboard', slug)
            else:
                if len(email_or_id) == 7:
                    if email_or_id.isalnum():
                        print('id')
                        nuevo_usuario = AstradUser.objects.get(cdunico=email_or_id)
                        board.linked_users.add(nuevo_usuario)
                        board.save()
                        messages.success(request, 'The item has been created. 2')
                        return redirect('boards:userboard', slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
            return redirect('boards:userboard', slug)
    # else:
    #     messages.success(request, 'Ha ocurrido un error inesperado')
    #     return redirect('boards:userboard', slug)
    
    usersboards = Permit.objects.filter(board = board )
    form = userboardForm()
    # Lista para almacenar la información de los usuarios como diccionarios
    lista_usuarios = []
    # Iterar sobre los usuarios vinculados y formar el diccionario
    for usuario in usersboards:
        usuario_dict = {
            'inicial': usuario.user.username[0] if usuario.user.username else '' ,
            'username': usuario.user.username,
            'email': usuario.user.email,
        }
        lista_usuarios.append(usuario_dict)
        

    return render(request, './boards/userboard.html', {
        'lista_usuarios': lista_usuarios,
        'form': form,
    })