from django.shortcuts import render ,redirect ,get_object_or_404
from common.models import Service ,Roomie , Guest ,Calculation
from bills.forms.serviceform import ServiceForm
from bills.forms.roomieform import RoomieForm
from bills.forms.guestform import GuestForm

from django.contrib import messages
from django.http import JsonResponse
from .calculate import calcular_precio_recibo ,generar_informe
from components.humaniza import format_value_float
from django.contrib.auth.decorators import login_required
import openpyxl
from django.http import HttpResponse


from django.views.decorators.csrf import csrf_protect
import json

@login_required
def service(request):
    user = request.user
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            cost = form.cleaned_data['cost']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            payment_date = form.cleaned_data['payment_date']
            
            Service.objects.create(
                user = user,
                name = name, 
                cost = cost,
                start_date = start_date,
                end_date = end_date,
                payment_date = payment_date,
            )
            messages.success(request, 'El servicio ha sido creado.')
            return redirect('bills:service')
        else:
            messages.error(request, 'Error en la creación de servicio.')
            return redirect('bills:service')   
    else : 
        services = Service.objects.filter(user = user ).order_by('-id')
        form = ServiceForm()
    return render(request, './bills/service.html' , {
                                                        'form' : form,
                                                        'services' : services,
                                                        
                                                        })
    
@login_required
def calculator(request,id):
    visitante = []
    acumulados = {}
    total = 0
    service = Service.objects.get(pk=id)
    user = request.user
    if request.method == 'POST':
        
        ## create Roomie
        
        form1 = RoomieForm(request.POST, prefix='form1')
        if form1.is_valid():
            form1_data = form1.cleaned_data      
            
            Roomie.objects.create(
                user = user,
                name = form1_data['name'],
            )
            messages.success(request, 'El Ocupante ha sido creado.')
            return redirect('bills:calculator',id)
        else:
            for field, errors in form1.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
        
        
        ## create Guest 
        
        form2 = GuestForm(request.POST, request.FILES, prefix='form2')
        if form2.is_valid():
            form2_data = form2.cleaned_data
            roomie = get_object_or_404(Roomie, pk= form2_data['roomie'] ) 
            
            Guest.objects.create(
                    name = form2_data['name'],
                    roomie = roomie,
                    service = service,
                    arrival_date = form2_data['arrival_date'], 
                    departure_date = form2_data['departure_date'],
                )
            messages.success(request, 'El Visitante ha sido creado.')
            return redirect('bills:calculator',id)
        else:
            for field, errors in form1.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
        
            
            
    else :
        ocupantes = Roomie.objects.filter(user = user)
        
        for data in ocupantes:
            visitante = Guest.objects.filter(roomie = data ,service = service)
            
            ocu = data.id
            if ocu not in acumulados:
                acumulados[ocu] = {
                'name':data.name,
                'pago': 0,
                'visitante':[],
                'nvisitante':0,
            }
            
            for v in visitante:
                acumulados[ocu]['visitante'].append(v.name)  
                
            if service.closet == False :
                acumulados[ocu]['pago'] = 0
            else:
                calculation = Calculation.objects.get(roomie = data ,service = service)
                if calculation :
                    acumulados[ocu]['pago'] = calculation.value
                

            acumulados[ocu]['nvisitante'] = len(acumulados[ocu]['visitante'])
            total += len(acumulados[ocu]['visitante'])
        
        ocupantes = list(acumulados.values()) 
        form1 = RoomieForm(prefix='form1')
        form2 = GuestForm(prefix='form2',custom_id=user.id)
    
    
    return render(request, './bills/calculator.html' , {
                                                        'form1' : form1,
                                                        'form2' : form2,
                                                        'service' : service,
                                                        'ocupantes':ocupantes,
                                                        'visitante':visitante,
                                                        'total':total,
                                                        
                                                        })



@csrf_protect
def closet(request):

    if request.method == 'POST':
        try:
            service_id = request.POST.get('service_id', '')  # Obtén el ID desde el cuerpo de la solicitud
            if not service_id:
                return JsonResponse({'status': 'error', 'message': 'ID no proporcionado'}, status=400)
            
            service = get_object_or_404(Service, pk=service_id)
            user = request.user
            
            ocupantes = Roomie.objects.filter(user=user)
            
            ocupantes_list = []

            for data in ocupantes:
                visitante = Guest.objects.filter(roomie=data, service=service)
                invitados = [
                    {
                        'fecha_inicio': str(v.arrival_date),
                        'fecha_fin': str(v.departure_date)
                    } for v in visitante
                ]
                
                ocupantes_list.append({
                    'nombre': data.name,
                    'id': data.id,
                    'invitados': invitados
                })

            result = {
                'fecha_inicio_servicio': str(service.start_date),
                'fecha_fin_servicio': str(service.end_date),
                'valor_servicio_mensual': int(service.cost),
                'ocupantes': ocupantes_list
            }
            
            data2 = calcular_precio_recibo(result) 
            
            # Crear un diccionario para acceso rápido a los resultados por nombre
            resultados_dict = {res['nombre']: res['total_a_pagar'] for res in data2['resultados']}
            
            for ocupante in ocupantes_list:
                nombre = ocupante['nombre']
                total_a_pagar = resultados_dict.get(nombre, 0)  # Obtener el valor total a pagar, por defecto 0 si no se encuentra
                roomie = get_object_or_404(Roomie, pk=ocupante['id'])
                
                # Crear la instancia de Calculation con el valor correcto
                data = Calculation(
                    roomie=roomie,
                    service=service,
                    value=total_a_pagar,
                )
                data.service.closet = True
                data.service.save()
                data.save()
            
            return JsonResponse({'status': 'ok'})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Error en los datos de la solicitud'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)




@login_required
def report(request, id):
    service = Service.objects.get(pk=id)
    user = request.user

    ocupantes = Roomie.objects.filter(user=user)

    ocupantes_list = []

    for data in ocupantes:
        visitante = Guest.objects.filter(roomie=data, service=service)
        invitados = [
            {
                'fecha_inicio': str(v.arrival_date),
                'fecha_fin': str(v.departure_date)
            } for v in visitante
        ]

        ocupantes_list.append({
            'nombre': data.name,
            'id': data.id,
            'invitados': invitados
        })

    result = {
        'fecha_inicio_servicio': str(service.start_date),
        'fecha_fin_servicio': str(service.end_date),
        'valor_servicio_mensual': int(service.cost),
        'ocupantes': ocupantes_list
    }

    data = generar_informe(result)
    # return JsonResponse(data)
    

    # Crear un workbook y una hoja
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Datos'

    # Añadir encabezados
    headers = ["Fecha"] + list(next(iter(data.values())).keys())
    sheet.append(headers)

    # Añadir los datos
    for date, values in data.items():
        row = [date] + [values.get(name, 0) for name in headers[1:]]
        sheet.append(row)

    # Configurar la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=datos.xlsx'

    # Guardar el workbook en la respuesta
    workbook.save(response)
    return response






