from django.urls import path

from .views.boards import boards
from .views.viewboard import viewboard

urlpatterns = [
    path('boards/', boards.boards, name='boards'),
    path('boards/<str:slug>', viewboard.viewboard, name='viewboard'),
]