from django.urls import path
from .views.shoppinglists import shoppinglists


urlpatterns = [
    path('boards/lists/', shoppinglists.shoppinglists, name='shoppinglists'),
    path('boards/lists/<int:idlist>/', shoppinglists.shoppinglistsviews, name='shoppinglistsviews'),
    path('update-item/<int:item_id>/', shoppinglists.update_item_status, name='update_item_status'),
    path('update-price/<int:item_id>/', shoppinglists.update_price, name='update_price'),
]