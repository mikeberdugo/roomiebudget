from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from common.models import Board, Patrimony
from patrimony.form.passivesform import passivesform
from patrimony.form.assetsform import assetsform
from components.humaniza import format_value_float



def passives(request, slug):
    board = Board.objects.get(slug=slug)
    user = request.user

    if request.method == 'POST':
        # Procesar los datos del formulario 1
        form1 = passivesform(request.POST, prefix='form1')
        if form1.is_valid():
            form1_data = form1.cleaned_data
            Patrimony.objects.create(
                user=user,
                name=form1_data['name'],
                balance=form1_data['balance'],
                currency=form1_data['currency'],
                patrimony_type=form1_data['patrimony_type'],
                status=form1_data['status'],
                board=board,
                type_dos=2,
            )
            messages.success(request, 'The Passives have been created.')
            return redirect('patrimony:passives', slug)
        else:
            for field, errors in form1.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')

        # Procesar los datos del formulario 2
        form2 = assetsform(request.POST, request.FILES, prefix='form2')
        if form2.is_valid():
            form2_data = form2.cleaned_data
            Patrimony.objects.create(
                user=user,
                name=form2_data['name'],
                balance=form2_data['balance'],
                currency=form2_data['currency'],
                patrimony_type=form2_data['patrimony_type'],
                status=form2_data['status'],
                board=board,
                type_dos=1,
            )
            messages.success(request, 'The Assets have been created.')
            return redirect('patrimony:passives', slug)
        else:
            for field, errors in form2.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')

    else:
        asserts = Patrimony.objects.filter(board=board, type_dos=1)
        passives = Patrimony.objects.filter(board=board, type_dos=2)
        patrimony = Patrimony.objects.filter(board=board)

        total_activos = asserts.aggregate(total=Sum('balance'))['total'] or 0
        
        total_pasivos = passives.aggregate(total=Sum('balance'))['total'] or 0
        
        total = total_activos + total_pasivos
        porcentaje_activos = (total_activos / total) * 100
        porcentaje_pasivos = (total_pasivos / total) * 100
        
        
        total_activos = format_value_float(total_activos)
        total_pasivos = format_value_float(total_pasivos)
        
        form1 = passivesform(prefix='form1')
        form2 = assetsform(prefix='form2')
        
        
        

    return render(request, './patrimony/patrimony.html', {
        'form1': form1,
        'form2': form2,
        'asserts': asserts,
        'passives': passives,
        'patrimony': patrimony,
        'total_activos': total_activos,
        'total_pasivos': total_pasivos,
        'porcentaje_activos': porcentaje_activos,
        'porcentaje_pasivos': porcentaje_pasivos,
    })
