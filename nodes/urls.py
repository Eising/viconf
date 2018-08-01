from django.urls import path

from . import views

app_name = 'nodes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('node/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('node/<int:pk>/interfaces/', views.NodeInterfaceView.as_view(), name='nodeinterfaces'),
    path('node/<int:pk>/edit/', views.NodeUpdateView.as_view(), name='nodeedit'),
    path('node/<int:node_id>/delete/', views.node_delete, name="delete"),
    path('node/new', views.NodeCreateView.as_view(), name='newnode'),
    path('groups/', views.GroupView.as_view(), name='groups'),
    path('groups/new', views.GroupCreateView.as_view(), name='newgroup'),
    path('groups/<int:pk>/', views.GroupDetailView.as_view(), name='groupview'),
    path('sites/', views.SiteView.as_view(), name='sites'),
    path('sites/new', views.SiteCreateView.as_view(), name='newsite'),
    path('sites/<int:pk>/', views.SiteDetailView.as_view(), name='siteview'),
    path('sites/<int:pk>/edit/', views.SiteUpdateView.as_view(), name='siteedit'),
    path('sites/<int:pk>/delete/', views.site_delete, name='sitedelete')
]
