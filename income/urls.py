from django.urls import path
from .views.Transaction import Transaction
from .views.typeTransaction import typeTransaction

urlpatterns = [
    path('<str:slug>/Transaction/', Transaction.Transactions, name='Transaction'),
    path('<str:slug>/typeTransaction/', typeTransaction.typeTransactions, name='typeTransaction'),
    
    #path('boards/lists/<int:idlist>/', shoppinglists.shoppinglistsviews, name='shoppinglistsviews'),
]