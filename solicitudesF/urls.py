# PROYECTO/solicitudesF/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'solicitudesF'

urlpatterns = [
    path('', views.home, name='home'),
    path('nueva/', views.crear_solicitud, name='crear_solicitud'),
    path('exitosa/', views.solicitud_exitosa, name='solicitud_exitosa'),
    path('listar/', views.listar_tipos_solicitud, name='listar_tipos_solicitud'),
    path('listado/', views.lista_solicitudes, name='listado'), # La clave es este "name"
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='solicitudesF:home'), name='logout'),
    path('mis-solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),
    path('solicitud/<int:solicitud_id>/', views.detalle_solicitud, name='detalle_solicitud'),
]