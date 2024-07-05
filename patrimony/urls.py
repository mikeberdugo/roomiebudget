from django.urls import path
from .views.assets import assets
from .views.Passives import passives



urlpatterns = [
    path('<str:slug>/assets/', assets.assets, name='assets'),
    path('<str:slug>/patrimony/', passives.passives, name='passives'),
    #path('boards/lists/<int:idlist>/', shoppinglists.shoppinglistsviews, name='shoppinglistsviews'),
]