from django.urls import path
from .views import (item_list, manage_items,
                    item_new, add_to_cart,
                    remove_from_cart, OrderSummaryView,
                    ItemDetailView, Dif, AutoDif, Candle)


app_name = 'core'
urlpatterns = [
    path('', item_list, name='item-list'),
    path('manage/', manage_items, name='manage'),
    path('item/new/', item_new, name='item_new'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('box/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='item'),
    path('dif/', Dif.as_view(), name='dif'),
    path('autodif/', AutoDif.as_view(), name='autodif'),
    path('candle/', Candle.as_view(), name='candle'),
    ]
