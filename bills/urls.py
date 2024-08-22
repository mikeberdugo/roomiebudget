from django.urls import path
from .views.bills import bills
from .views.service import service


urlpatterns = [
    path('bills', bills.bills, name='bills'),
    path('service', service.service, name='service'),
    path('service/<str:id>', service.calculator, name='calculator'),
    path('service/closet/service', service.closet, name='closet'),
    path('service/<str:id>/api1', service.api1, name='api1'),
]