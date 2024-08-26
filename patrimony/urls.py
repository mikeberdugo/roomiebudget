from django.urls import path
from .views.assets import assets
from .views.Passives import passives



urlpatterns = [
    path('assets/', assets.assets, name='assets'),
    path('patrimony/', passives.passives, name='passives'),
    #path('boards/lists/<int:idlist>/', shoppinglists.shoppinglistsviews, name='shoppinglistsviews'),
]