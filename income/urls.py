from django.urls import path
from .views.Transaction import Transaction


urlpatterns = [
    path('<str:slug>/Transaction/', Transaction.Transactions, name='Transaction'),
    #path('boards/lists/<int:idlist>/', shoppinglists.shoppinglistsviews, name='shoppinglistsviews'),
]