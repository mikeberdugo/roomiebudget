from django.urls import path
from .views.shoppinglists import shoppinglists
from .views.budget import budget

urlpatterns = [
    path('lists/', shoppinglists.shoppinglists, name='shoppinglists'),
    path('lists/<int:idlist>/', shoppinglists.shoppinglistsviews, name='shoppinglistsviews'),
    path('update-item-shoppinglist/<int:item_id>/', shoppinglists.update_item_status, name='update_item_status'),
    path('update-price/<int:item_id>/', shoppinglists.update_price, name='update_price'),
    
    ## budget
    
    path('<str:slug>/budget/', budget.budget, name='budget'),
    path('<str:slug>/budget/<int:idbudget>/', budget.budgetitems, name='budgetitems'),
    path('update-item-budget/<int:item_id>/', budget.update_item_status, name='budget_update_item_status'),
]