from django.urls import path
from .views.apartment import apartment

urlpatterns = [
    path('apartment/', apartment.apartment_home, name='apartment_home'),
    path('apartment/add', apartment.apartment_home_add, name='apartment_home_add'),
    path('apartment/view/<str:id>', apartment.apartment_view, name='apartment_view'),
    
]