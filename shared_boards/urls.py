from django.urls import path

from .views.boards import boards
from .views.createboards import createboard
from .views.viewboard import viewboard

urlpatterns = [
    path('boards/', boards.boards, name='boards'),
    path('boards/create', createboard.createboard, name='createboard'),
    path('boards/<str:slug>', viewboard.viewboard, name='viewboard'),
    # path('logout/', views.logout_view, name='logout'),
    # path('prueba/', views.prueba, name='prueba'),
]