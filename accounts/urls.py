from django.urls import path

from .views.accounts import accounts

urlpatterns = [
    path('boards/<str:slug>/accounts', accounts.accounts, name='account'),
    
]