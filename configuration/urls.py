from django.urls import path

from . import views

app_name = 'configuration'

urlpatterns = [
    path('', views.ProvisionList.as_view(), name='provision'),
    path('forms/', views.FormList.as_view(), name='forms'),
    path('templates/', views.TemplateList.as_view(), name='templates'),
    path('templates/compose', views.TemplateCreate.as_view(), name='templatecompose'),
    path('templates/<int:pk>/tags', views.TemplateTags.as_view(), name='templatetags'),
    path('templates/<int:pk>/', views.TemplateView.as_view(), name='templateview'),
    path('templates/<int:pk>/clone', views.template_clone, name='templateclone'),
    path('templates/<int:pk>/delete', views.TemplateDelete.as_view(), name='templatedelete')

]
