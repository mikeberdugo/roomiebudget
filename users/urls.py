from django.urls import path

from .views.login import login
from .views.index import index

urlpatterns = [
    path('', login.login_user, name='login'),
    path('index', index.login_index, name='index'),
    
    # path('logout/', views.logout_view, name='logout'),
    # path('prueba/', views.prueba, name='prueba'),
]