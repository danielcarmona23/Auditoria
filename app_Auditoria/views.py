from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse, HttpResponse
from django.urls import reverse
from django.db.models import Sum,Q

from app_Auditoria.models import *
from django.contrib.auth import login as auth_login,logout,authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction,connections
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage, send_mail
from Auditoria.settings import EMAIL_HOST_USER


# @login_required
def principal(request):
	return render(request,'principal.html')

def login(request):
	m=''
	if request.method == 'POST':
		
		usuarionombre = request.POST.get('usuarionombre')
		passw = request.POST.get('passw')
		usuario = authenticate(username=usuarionombre,password=passw)
		if usuario is not None:
			if usuario.is_active:
				auth_login(request,usuario)
				return redirect('app_Auditoria:principal')
			else:
				m = 'USUARIO INACTIVO'
				return render(request,'login.html',{'m':m})
		else:
			m = 'USUARIO O CONTRASEÑA INCORRECTO'
			return render(request,'login.html',{'m':m})

	return render(request,'login.html')

@login_required
def cerrar_sesion(request):
	logout(request)
	return HttpResponseRedirect(reverse('app_Auditoria:login'))
	

def registro_paciente(request):
	

	if request.user.is_authenticated:
		pacientes = Paciente.objects.all()
		generos = Genero.objects.all()
		ret_data,query_paciente,errores = {},{},{}

		if request.method == 'POST':
			
			
			
			
			if request.POST.get('identidad') == '':
				errores['identidad'] = "Debe ingresar la Identidad"

			else:
				query_paciente["identidad"] = request.POST.get('identidad')


			if request.POST.get('nombres') == '':
				errores['nombres'] = "Debe ingresar sus Nombres"

			else:
				query_paciente["nombres"] = request.POST.get('nombres')


			if request.POST.get('apellidos') == '':
				errores['apellidos'] = "Debe ingresar sus Apellidos"

			else:
				query_paciente["apellidos"] = request.POST.get('apellidos')


			if request.POST.get('telefono') == '':
				errores['telefono'] = "Debe ingresar su Telefono"

			else:
				query_paciente["telefono"] = request.POST.get('telefono')

			if request.POST.get('direccion') == '':
				errores['direccion'] = "Debe ingresar su Direccion"

			else:
				query_paciente["direccion"] = request.POST.get('direccion')

			

			if request.POST.get('genero') == '':
				errores['genero'] = "Debe ingresar el Genero"
				
			else:
				query_paciente["genero"] = Genero.objects.get(pk=int(request.POST.get("genero")))
			
			
			print (errores)

			if not errores:

				try:
					
					
					pac = Paciente(**query_paciente)
					pac.save()


				except Exception as e:
					transaction.rollback()
					errores['administrador'] = e
					print (e)
					ctx = {'errores':errores, 'generos': generos, 'pacientes':pacientes }

					return render(request,'registro_paciente.html',ctx)
				else:
					transaction.commit()
					return HttpResponseRedirect(reverse('app_Auditoria:registro_paciente')+'?ok')
			else:
				ctx = {'errores':errores, 'generos': generos, 'pacientes':pacientes }
				return render(request,'registro_paciente.html',ctx)
		else:
			ctx = {'errores':errores, 'generos': generos, 'pacientes':pacientes }
			return render(request,'registro_paciente.html',ctx)
	else:
		return redirect('app_Auditoria:principal')


def registro_doctor(request):
	

	if request.user.is_authenticated:
		doctores = Doctor.objects.all()
		generos = Genero.objects.all()
		ret_data,query_doctor,errores = {},{},{}

		m = request.POST.get('correo')
		list_correo = []
		r = 0
		username = ''
		password = ''

		if request.method == 'POST':
			
				
			if request.POST.get('correo') == '':					
				errores['correo'] = "Debe ingresar su Correo"				
			elif User.objects.filter(email = m).exists():					
				errores['correo'] = "Correo ya existente"				
			else:					
				query_doctor["correo"] = request.POST.get('correo')									
				list_correo.append(m)					
				r = m.find('@') 					
				for i in range(0,r):						
					username += m[i]

				password = username
			
			
			if request.POST.get('identidad') == '':
				errores['identidad'] = "Debe ingresar la Identidad"

			else:
				query_doctor["identidad"] = request.POST.get('identidad')


			if request.POST.get('nombres') == '':
				errores['nombres'] = "Debe ingresar sus Nombres"

			else:
				query_doctor["nombres"] = request.POST.get('nombres')


			if request.POST.get('apellidos') == '':
				errores['apellidos'] = "Debe ingresar sus Apellidos"

			else:
				query_doctor["apellidos"] = request.POST.get('apellidos')


			if request.POST.get('telefono') == '':
				errores['telefono'] = "Debe ingresar su Telefono"

			else:
				query_doctor["telefono"] = request.POST.get('telefono')

			if request.POST.get('direccion') == '':
				errores['direccion'] = "Debe ingresar su Direccion"

			else:
				query_doctor["direccion"] = request.POST.get('direccion')

			if request.POST.get('correo') == '':
				errores['correo'] = "Debe ingresar su Email"

			else:
				query_doctor["correo"] = request.POST.get('correo')

			

			if request.POST.get('genero') == '':
				errores['genero'] = "Debe ingresar el Genero"
				
			else:
				query_doctor["genero"] = Genero.objects.get(pk=int(request.POST.get("genero")))
			
			
			print (errores)

			if not errores:

				try:
					
					#Creación de usuario						
					User.objects.create_user(username, m, password)						
					user = User.objects.last()						
					#guardar usuario par el vendendor 						
					query_doctor['usuario'] = user
					doc = Doctor(**query_doctor)
					doc.save()
					
													
					message = 'Usuario : ' + username ,
					'Password: ' + password						
					recepient = m						
					send_mail( message, EMAIL_HOST_USER, [recepient], fail_silently = False)


				except Exception as e:
					transaction.rollback()
					errores['administrador'] = e
					print (e)
					ctx = {'errores':errores, 'generos': generos, 'doctores':doctores }

					return render(request,'registro_doctor.html',ctx)
				else:
					transaction.commit()
					return HttpResponseRedirect(reverse('app_Auditoria:registro_doctor')+'?ok')
			else:
				ctx = {'errores':errores, 'generos': generos, 'doctores':doctores }
				return render(request,'registro_doctor.html',ctx)
		else:
			ctx = {'errores':errores, 'generos': generos, 'doctores':doctores }
			return render(request,'registro_doctor.html',ctx)
	else:
		return redirect('app_Auditoria:principal')


#CITAS
def registro_Cita(request):
	

	if request.user.is_authenticated:
		citas = Cita.objects.all()
		pacientes = Paciente.objects.all()
		doctores = Doctor.objects.all()
		ret_data,query_doctor,errores = {},{},{}

		

		if request.method == 'POST':
			
				
			if request.POST.get('paciente') == '':
				errores['paciente'] = "Debe ingresar el paciente"
				
			else:
				query_doctor["paciente"] = Paciente.objects.get(pk=int(request.POST.get("paciente")))
			
			#Doctor
			if request.POST.get('doctor') == '':
				errores['doctor'] = "Debe ingresar el doctor"
				
			else:
				query_doctor["doctor"] = Doctor.objects.get(pk=int(request.POST.get("doctor")))
				
				d= Doctor.objects.get(pk = int(request.POST.get("doctor")))
				print(d.usuario)
			

			if request.POST.get('estado') == '':
				errores['estado'] = "Debe ingresar el estado"

			else:
				query_doctor["estado"] = request.POST.get('estado')


			
			
			print (errores)

			if not errores:

				try:
					print('guardo')
					# Ci = Doctor(**query_doctor)
					# Ci.save()


				except Exception as e:
					transaction.rollback()
					errores['administrador'] = e 
					print (e)
					ctx = {'errores':errores, 'citas': citas, 'doctores':doctores ,'pacientes':pacientes}

					return render(request,'registro_Cita.html',ctx)
				else:
					transaction.commit()
					return HttpResponseRedirect(reverse('app_Auditoria:registro_Cita')+'?ok')
			else:
				ctx = {'errores':errores, 'citas': citas, 'doctores':doctores ,'pacientes':pacientes}
				return render(request,'registro_Cita.html',ctx)
		else:
			ctx = {'errores':errores, 'citas': citas, 'doctores':doctores ,'pacientes':pacientes}
			return render(request,'registro_Cita.html',ctx)
	else:
		return redirect('app_Auditoria:principal')