from django.urls import path

from .views.boards import boards
from .views.createboards import createboard


urlpatterns = [
    path('boards/', boards.boards, name='boards'),
    path('boards/create', createboard.createboard, name='createboard'),
    # path('logout/', views.logout_view, name='logout'),
    # path('prueba/', views.prueba, name='prueba'),
]