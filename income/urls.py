from django.urls import path
from .views.Transaction import Transaction


urlpatterns = [
    path('boards/Transaction/', Transaction.Transaction, name='Transaction'),
    #path('boards/lists/<int:idlist>/', shoppinglists.shoppinglistsviews, name='shoppinglistsviews'),
]