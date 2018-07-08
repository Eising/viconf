from django.urls import path

from . import views

app_name = 'configuration'

urlpatterns = [
    path('', views.ProvisionList.as_view(), name='provision'),
    path('templates/', views.TemplateList.as_view(), name='templates'),
    path('templates/compose', views.TemplateCreate.as_view(), name='templatecompose'),
    path('templates/<int:template_id>/tags', views.template_tags, name='templatetags'),
    path('templates/<int:pk>/', views.template_view, name='templateview'),
    path('templates/<int:pk>/edit', views.TemplateUpdate.as_view(), name='templateedit'),
    path('templates/<int:pk>/clone', views.TemplateUpdate.as_view(), name='templateclone'),
    path('templates/<int:pk>/delete', views.template_delete, name='templatedelete'),
    path('forms/', views.form_list, name='forms'),
    path('forms/compose', views.form_create, name='formcompose'),
    path('forms/config', views.form_config, name='formconfig'),
    path('forms/<int:pk>/', views.form_view, name='formview'),
    path('forms/<int:pk>/delete', views.form_delete, name='formdelete'),
    path('forms/<int:pk>/update', views.form_create, name='formupdate')

]
