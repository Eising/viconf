from django.urls import path

from . import views

app_name = 'provisioning'
urlpatterns = [
    path('service/<int:pk>/up/', views.provision_up, name='up'),
    path('service/<int:pk>/down/', views.provision_down, name='down'),
    path('task/<int:pk>/', views.view_task, name='view'),
    path('task/<int:pk>/commit', views.commit_task, name='commit')
]
