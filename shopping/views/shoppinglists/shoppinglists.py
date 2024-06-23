from django.shortcuts import render, redirect
from common.models import ShoppingList , ListItem
from shopping.forms.ShoppingListForm  import ShoppingListForm  
from django.contrib import messages
from shopping.forms.ListItemForm import ListItemForm


def shoppinglists(request):
    if request.method == 'POST':
        form = ShoppingListForm(request.POST)
        if form.is_valid():

            ShoppingList.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description']
            )
            messages.success(request, 'the list has been created.')
            return redirect('shopping:shoppinglists')
        else:
            messages.error(request, 'list creation failure.')
            return redirect('shopping:shoppinglists')
    else:
        lists = ShoppingList.objects.all()
        form  = ShoppingListForm() 
    
    return render(request, './shopping/shoppinglists.html' , 
                    {'lists':lists,
                    'form' : form , 

                    })
    
def shoppinglistsviews(request,idlist):
    if request.method == 'POST':
        # Obtener los datos del formulario
        form = ShoppingListForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            purchased = form.cleaned_data['purchased']
    else: 
        list = ShoppingList.objects.get(id = idlist )
        listitems = ListItem.objects.filter(shopping_list = list)
        form = ListItemForm()
    
    
    
    return render(request, './shopping/shoppinglistsviews.html' , 
                    {'listitems':listitems,
                    'form' : form , 
                    })