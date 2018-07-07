from django.urls import path

from . import views

app_name = 'configuration'

urlpatterns = [
    path('templates/', views.TemplateList.as_view(), name='templates'),
    path('templates/compose', views.TemplateCreate.as_view(), name='templatecompose'),
    path('templates/<int:template_id>/tags', views.template_tags, name='templatetags'),
    path('templates/<int:pk>/', views.template_view, name='templateview'),
    path('templates/<int:pk>/edit', views.TemplateUpdate.as_view(), name='templateedit'),
    path('templates/<int:pk>/clone', views.TemplateUpdate.as_view(), name='templateclone'),
    path('templates/<int:pk>/delete', views.template_delete, name='templatedelete')

]
