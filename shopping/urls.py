from django.urls import path
from .views.shoppinglists import shoppinglists


urlpatterns = [
    path('boards/lists/', shoppinglists.shoppinglists, name='shoppinglists'),
    path('boards/lists/<int:idlist>/', shoppinglists.shoppinglistsviews, name='shoppinglistsviews'),
]