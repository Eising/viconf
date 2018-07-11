from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('service/<int:pk>/push/<str:direction>', views.configure_device, name='push'),
    path('<int:pk>/', views.view_task, name='view'),
    path('<uuid:pk>/commit', views.confirm_task, name='commit')
]
