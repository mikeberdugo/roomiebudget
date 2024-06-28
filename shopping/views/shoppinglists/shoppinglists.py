from django.shortcuts import render, redirect ,  get_object_or_404
from common.models import ShoppingList , ListItem
from shopping.forms.ShoppingListForm  import ShoppingListForm  
from django.contrib import messages
from shopping.forms.ListItemForm import ListItemForm
from django.http import JsonResponse



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
        lists = ShoppingList.objects.get(id = idlist )        
        form = ListItemForm(request.POST)
        if form.is_valid():
            
            ListItem.objects.create(
                shopping_list = lists,
                name=form.cleaned_data['name'],
                price = float (form.cleaned_data['price']),
                purchased = form.cleaned_data['purchased']
            ) 
            messages.success(request, 'the Item has been created.')
            return redirect('shopping:shoppinglistsviews',idlist)
        else:
            messages.error(request, 'Item creation failure.')
            return redirect('shopping:shoppinglistsviews',idlist)           
    else: 
        lists = ShoppingList.objects.get(id = idlist )
        listitems = ListItem.objects.filter(shopping_list = lists)
        form = ListItemForm()
    
    
    
    return render(request, './shopping/shoppinglistsviews.html' , 
                    {'listitems':listitems,
                    'form' : form , 
                    })
    
    
def update_item_status(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ListItem, id=item_id)
        item.purchased = not item.purchased
        item.save()
        item.shopping_list.save()
        return JsonResponse({'success': True, 'purchased': item.purchased})
    return JsonResponse({'success': False})

def update_price(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ListItem, id=item_id)
        new_price = request.POST.get('price', '')
        if new_price:
            new_price = round(float(new_price), 2)
            item.price = new_price
            item.save()
            return JsonResponse({'success': True, 'price': item.price})
    return JsonResponse({'success': False})