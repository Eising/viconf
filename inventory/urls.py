from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.view_inventories, name='index'),
    path('add/', views.add_inventory, name='addinventory'),
    path('<int:pk>/', views.view_inventory, name='viewinventory'),
    path('<int:pk>/row/add', views.add_row, name='addrow'),
    path('<int:pk>/row/<int:row_id>/delete', views.delete_inventory_row, name='deleterow'),
    path('<int:pk>/delete/', views.delete_inventory, name='deleteinventory'),
    path('json/row/update/', views.update_row, name='jsonupdaterow')
]
