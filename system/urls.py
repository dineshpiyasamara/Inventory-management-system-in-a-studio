from django.urls import path
from system.views import *

urlpatterns = [
    path('', home, name='home'),
    path('inventory/', inventory, name='inventory'),
    path('sell-items/', sell, name='sell'),
    path('purchase-items/', purchase, name='purchase'),
    path('employees/', employees, name='employees'),

    path('other-item-json/<str:product>/',
         json_item_data_others, name='other-item-json'),
]
