from django.urls import path


from . import views

app_name = 'app_Auditoria'

urlpatterns = [
 path('', views.login, name='login'),	
 path('principal', views.principal, name='principal'),
 path('cerrar_sesion', views.cerrar_sesion, name='cerrar_sesion'),
 path('registro/paciente', views.registro_paciente, name='registro_paciente'),
 path('registro/doctor', views.registro_doctor, name='registro_doctor'),
 path('registro/Cita', views.registro_Cita, name='registro_Cita'),
]