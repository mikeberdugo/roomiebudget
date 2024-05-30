from django.urls import path

from .views.login import login

urlpatterns = [
    path('', login.login_user, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    # path('prueba/', views.prueba, name='prueba'),
]