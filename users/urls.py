from django.urls import path

from .views.login import access
from .views.index import index

urlpatterns = [
    path('', access.login_view, name='login'),
    path('logout/', access.logout_view, name='logout'),
    path('signup/', access.signup_view, name='signup'),
    #path('home/', index.index_login , name='home'),
    
    # path('logout/', views.logout_view, name='logout'),
    # path('prueba/', views.prueba, name='prueba'),
]