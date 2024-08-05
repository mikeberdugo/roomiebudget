from django.urls import path


from .views import index

urlpatterns = [
    path('home/', index , name='home'),
    
    # path('logout/', views.logout_view, name='logout'),
    # path('prueba/', views.prueba, name='prueba'),
]