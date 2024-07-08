from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from common.models import Board, Budget , BudgetItem
from components.humaniza import format_value_float
from shopping.forms.budgetForm import budgetForm 
from shopping.forms.budgetitemsForm import budgetitemsForm  
from django.http import JsonResponse
from django.db.models import Sum


def budget(request, slug):
    
    
    board = Board.objects.get(slug=slug)
    user = request.user
    
    if request.method == 'POST':
        form = budgetForm(request.POST)
        if form.is_valid():
            Budget.objects.create(
                board = board,
                user = user,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description']
            )
            messages.success(request, 'the Budget has been created.')
            return redirect('shopping:budget' ,slug)
        else:
            messages.error(request, 'Budget creation failure.')
            return redirect('shopping:budget' ,slug)
    
    else:
        form = budgetForm()
        budgets = Budget.objects.filter( board = board )
        
    return render(request, './shopping/budget.html', {
        'form':form,
        'budgets':budgets,
    })
    
def budgetitems(request, slug,idbudget):
    board = Board.objects.get(slug=slug)
    user = request.user
    budget = Budget.objects.get( id = idbudget )
    
    if request.method == 'POST':
        form = budgetitemsForm(request.POST)
        if form.is_valid():
            BudgetItem.objects.create(
                budget = budget,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                amount=form.cleaned_data['amount'],
                category=form.cleaned_data['category'],
            )
            messages.success(request, 'the Items has been created.')
            return redirect('shopping:budgetitems' , slug=slug , idbudget=budget.id )
        else:
            messages.error(request, 'Items creation failure.')
            return redirect('shopping:budgetitems' , slug=slug , idbudget=budget.id )
            
    else:
        form =budgetitemsForm()
        items = BudgetItem.objects.filter(budget__id = idbudget )
        budget = Budget.objects.get(id = idbudget )
        sumitems = items.aggregate(total=Sum('amount'))['total'] or 0
    
    return render(request, './shopping/budgetitems.html', {
        'form':form,
        'items':items,
        'sumitems':sumitems,
        'budget':budget,
    })
    
    
    
def update_item_status(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(BudgetItem, id=item_id)
        item.is_paid = not item.is_paid
        item.save()
        item.budget.save()
        return JsonResponse({'success': True, 'purchased': item.is_paid})
    return JsonResponse({'success': False})
