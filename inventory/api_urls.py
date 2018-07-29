from django.urls import path

from . import api_views as views

app_name = 'api_inventory'

urlpatterns = [
    path('v1/', views.api_view_inventories, name='list'),
    path('v1/name/<str:name>/', views.api_get_inventory_by_name, name='viewbyname'),
    path('v1/name/<str:name>/row/<int:rowid>/', views.api_get_inventory_row_by_name, name='rowbyname'),
    path('v1/<int:pk>/', views.api_get_inventory_by_id, name='viewbyid'),
    path('v1/<int:pk>/row/<int:rowid>/', views.api_get_inventory_row_by_id, name='rowbyid'),
]
