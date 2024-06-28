from django.urls import path
from .views.accounts import accounts



urlpatterns = [
    path('<str:slug>/accounts', accounts.accounts, name='accounts'),
    
]