from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from common.models import Apartment
from decimal import Decimal
# Create your views here.

### index login 




@login_required
def apartment_home(request):
    apartments = Apartment.get_apartments_by_user(request.user.id)
    return render(request, './apartment_manager/apartment_home.html' , {'apartments':apartments})



@login_required
def apartment_home_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        home_type = request.POST.get('type')
        rent_amount = request.POST.get('rent_amount')
        admin_fee = request.POST.get('admin_fee', 0)
        number_of_occupants = request.POST.get('number_of_occupants')
        number_of_rooms = request.POST.get('number_of_rooms')
        number_of_bathrooms = request.POST.get('number_of_bathrooms')
        includes_admin = request.POST.get('includes_admin') == 'on'
        has_parking = request.POST.get('has_parking') == 'on'

        if name and home_type and rent_amount and number_of_occupants and number_of_rooms and number_of_bathrooms:
            home = Apartment.objects.create(
                name=name,
                type=home_type,
                rent_amount = float(rent_amount.replace(',', '')) if rent_amount else 0.0 ,
                admin_fee=float(admin_fee.replace(',', '')) if admin_fee else 0.0,
                number_of_occupants=number_of_occupants,
                number_of_rooms=number_of_rooms,
                number_of_bathrooms=number_of_bathrooms,
                includes_admin=includes_admin,
                has_parking=has_parking
            )

            # Añadir el usuario que lo crea como miembro
            home.members.add(request.user)

            messages.success(request, "¡Hogar creado exitosamente!")
            return redirect('apartment:apartment_home')
        else:
            messages.error(request, "Por favor completa todos los campos obligatorios.")
    return render(request, './apartment_manager/partials/apartment_home_modal.html')





@login_required
def apartment_view(request, id):
    apartment = Apartment.objects.get(id = id)
    return render(request, './apartment_manager/apartment_view.html' , {'apartment':apartment})

