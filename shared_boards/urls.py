from django.urls import path

from .views.boards import boards


urlpatterns = [
    path('boards/', boards.boards, name='boards'),
    # path('logout/', views.logout_view, name='logout'),
    # path('prueba/', views.prueba, name='prueba'),
]