from django.urls import path
from .views import *


app_name = 'core'
urlpatterns = [
    path('', item_list, name='item-list'),
    path('manage/', ItemView.as_view(), name='manage'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('box/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='item'),
    path('dif/', Dif.as_view(), name='dif'),
    path('autodif/', AutoDif.as_view(), name='autodif'),
    path('candle/', Candle.as_view(), name='candle'),
    path('create/', index, name='index'),
    path('box/tgbot', tgbot, name='tgbot'),
    # path('order/', Order.as_view(), name='order'),
    path('ajax/crud/create/',  CreateCrudItem.as_view(), name='crud_ajax_create'),
    path('ajax/crud/update/',  UpdateCrudItem.as_view(), name='crud_ajax_update'),
    path('ajax/crud/delete/',  DeleteCrudItem.as_view(), name='crud_ajax_delete'),
    ]
