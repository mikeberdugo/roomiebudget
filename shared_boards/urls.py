from django.urls import path

from .views.boards import boards
from .views.viewboard import viewboard
from .views.users  import usersboard


urlpatterns = [
    path('boards/', boards.boards, name='boards'),
    path('boards/<str:slug>', viewboard.viewboard, name='viewboard'),
    path('boards/<str:slug>/users', usersboard.userboard, name='userboard'),
]