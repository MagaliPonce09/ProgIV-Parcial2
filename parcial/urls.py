"""
URL configuration for parcial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from cuentas import views
from alumnos.views import dashboard
from alumnos.views import alumno_pdf
from alumnos.views import dashboard, alumno_pdf, scraping_view


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    
    path('alumno/<int:id>/pdf/', alumno_pdf, name='alumno_pdf'),
    path('scraping/', scraping_view, name='scraping'),

]

