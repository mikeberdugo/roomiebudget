from django.urls import path


from .views import index,login_view

urlpatterns = [
    path('home/', index , name='home'),
    path('', login_view , name='login'),
    
    # path('logout/', views.logout_view, name='logout'),
    # path('prueba/', views.prueba, name='prueba'),
]