from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from . import views

app_name = "api"

urlpatterns = [
    path('config/', views.ConfigRequestList.as_view()),
    path('status/<uuid:pk>/', views.StatusRequestView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)