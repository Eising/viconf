"""viconf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('nodes/', include('nodes.urls')),
    path('api/v1/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),
    path('', include('configuration.urls')),
    path('search/', include('search.urls')),
    path('provisioning/', include('provisioning.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.djhtml'), name='login'),
    path('logout/', auth_views.logout, {'next_page': 'login'}, name='logout'),
    path('password/', auth_views.PasswordChangeView.as_view(template_name='auth/password.djhtml'), name='changepassword'),
    path('password/done', auth_views.PasswordChangeDoneView.as_view(template_name='auth/password_changed.djhtml'), name='password_change_done')

]
