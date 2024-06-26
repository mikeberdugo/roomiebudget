from django.urls import path
from .views.accounts import accounts



urlpatterns = [
    path('boards/accounts', accounts.accounts, name='accounts'),
    
]