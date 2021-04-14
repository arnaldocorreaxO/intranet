#
import IfxPy
#Django HTTP
from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse

#Django Autenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

#VIEWS GENERIC
from django.views.generic import ListView
from django.views.generic.detail import DetailView 
from django.views.generic.edit import (CreateView,UpdateView,DeleteView)

#JSON
import json as simplejson

#Excepciones
from django.db.utils import IntegrityError

#Modelos
from django.contrib.auth.models import User
from .models import *

#Forms
from .forms import PerfilForm
from usuarios.forms import *


def signup_view(request):
	"""Registro de Usuario"""
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		password_confirmation = request.POST['password_confirmation']

		if password != password_confirmation:
			return render(request, 'usuarios/registrar.html', {'error': 'Contraseñas no coinciden'})
		try:
			usuario = User.objects.create_user(username=username, password=password)
		except IntegrityError:
			return render(request, 'usuarios/registrar.html', {'error': 'Documento ya existe!'})

		usuario.first_name = request.POST['first_name']
		usuario.last_name = request.POST['last_name']
		usuario.email = request.POST['email']
		usuario.is_active = False
		usuario.save()

		perfil = Perfil(usuario=usuario)
		perfil.sede = request.POST['sede']
		perfil.legajo = request.POST['legajo']
		perfil.telefono = request.POST['telefono']
		perfil.genero = request.POST['genero']
		perfil.fec_nacimiento = request.POST['fec_nacimiento']
		perfil.estado_civil = request.POST['estado_civil']
		perfil.save()
		#return redirect('activate')
		return render(
					request=request,
					template_name='registration/login_activate.html',
					context={'usuario_id':usuario.id}
					)

	form = PerfilForm()
	return render(request, 'usuarios/registrar.html',{'form':form})

def activate_view(request):
	return render(request,'registration/login_activate.html')
	# return redirect('activate')

def login_view(request):
	"""Login de Usuario"""
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		print('********************************')
		user = authenticate(request,username =username, password=password)

		# if not user.is_active:
		#   return render(request,'usuarios/login.html',
		#       {'err':"""Su cuenta se encuentra deshabilitada. 
		#                           Para activar su cuenta favor solicite vía telefónica Interno 2234 ó 2291, ó al correo informatica@inc.gov.py"""})

		if user:
				if user.is_active:
					login(request,user)
					return redirect('publicacion:list')
				else:
					return render(
					request=request,
					template_name='registration/login_activate.html',
					context={'usuario_id':user.id}
					)
					#return render(request,'ver_sol_intra')
					#return redirect('activate')
					# return render(request,'usuarios/login.html',{'err':'Favor comuniquése al correo'})            
		else:
			return render(request,'usuarios/login.html',{'err':'Nombre de usuario o contraseña inválida!'}) 
	return render(request,'usuarios/login.html')

def logout_view(request):
	"""Logout de Usuario"""
	logout(request)
	return redirect('login')

class UsuarioPerfilDetail(LoginRequiredMixin,DetailView):
	model = Perfil
	template_name = 'usuarios/usuario_perfil_detail.html'
	slug_field = 'usuario_id'
	slug_url_kwarg = 'usuario_id'
	#form_class = PerfilForm

class UsuarioPerfilUpdate(LoginRequiredMixin, UpdateView):
	"""Update profile view."""

	#template_name = 'users/update_profile.html'
	model = Perfil
	second_model = User
	template_name = 'usuarios/usuario_perfil_form.html'
	form_class = PerfilForm
	second_form_class = UsuarioForm

	def get_object(self):
		"""Return user's profile."""
		return self.request.user.perfil
	# success_url = reverse_lazy('usuarios/detail')
	def get_success_url(self):
		usuario_id = self.request.user.id
		#print(usuario_id)
		return reverse('perfil-detail', kwargs={'usuario_id':usuario_id})
		# return reverse('detail', kwargs={'pk' : self.kwargs.get('pk',0),})
		#return reverse('detail')

	#fields = ['website', 'biography', 'phone_number', 'picture']
	def get_context_data(self,**kwargs):
		context = super(UsuarioPerfilUpdate,self).get_context_data(**kwargs)
		#pk = self.kwargs.get('pk',0)
		# perfil = self.model.objects.get(id=pk)
		
		#Podemos buscar el perfil de 2 formas 
		#1°
		perfil = self.model.objects.get(id=self.request.user.perfil.id)
		#2°
		# perfil = self.model.objects.get(usuario_id=self.request.user.id)
		
		usuario = self.second_model.objects.get(id=perfil.usuario_id)
		if 'form' not in context:
			context['form'] = self.form_class
		if 'form2' not in context:
			context['form2'] = self.second_form_class(instance=usuario)
		context['id'] = perfil
		return context

	def post(self,request,*args,**kwargs):
		self.object = self.get_object
		# id_perfil = kwargs['pk']
		# print('******************************')
		# print(self.request.user.perfil.id)
		# print('******************************')
		# id_perfil = self.model.objects.get(id=self.request.user.perfil.id)        
		#id_perfil = "36"
		perfil = self.model.objects.get(id=self.request.user.perfil.id)
		#perfil = self.model.objects.get(usuario=usuario_id)
		usuario = self.second_model.objects.get(id=perfil.usuario_id)
		form = self.form_class(request.POST,request.FILES,instance=perfil)
		form2 = self.second_form_class(request.POST,instance=usuario)
		"""     

		"""
		print (form.is_valid(), form.errors, type(form.errors))

		if form.is_valid() and form2.is_valid():
			form.save()
			form2.save()
			return HttpResponseRedirect(self.get_success_url())
			# return reverse('detail', kwargs={'pk' : self.object.pk})
		else:
			context = {}
			#return reverse('detail', kwargs={'pk' : self.kwargs.get('pk',0)},)
			# else:
			#   #return HttpResponseRedirect(self.get_success_url())
			#   #return HttpResponseRedirect('/')
			#   # return reverse('detail', kwargs={'pk' : self.object.pk})
			#form = PerfilForm(instance=perfil)
			#form2 = UsuarioForm(instance=usuario)
			
			# context.update(csrf(request))
			context.update(request)
			context['form'] = form
			context['form2'] = form2
			context['perfil'] = perfil
			print('************************************************')
			#   print (form.errors)
			return render(request, 'usuarios/usuario_perfil_form.html', context)
			#return self.form_invalid(form)


def ver_sol_intra(request,**kwargs): 
	user_id = kwargs['usuario_id']
	perfil = Perfil.objects.filter(usuario_id=user_id)  
	#print(context)
	return render(
			request=request,
			template_name='pdf/solicitud_intranet_pdf.html',
			context={'perfil':perfil}
	)
def choiceEmpleado(**Kwargs):
	
	#dpto_id = request.GET.get('id_dpto','1')
	sedeId = Kwargs['vSede']
	#print('*'*100)
	#print(sedeId)
	all_perfiles = []
	result_set = []
	#answer = str(dpto_id[1:-1])
	
	#selected_dpto = dpto_id
	#print ("selected dpto id", answer)	
	#all_ciudades =Perfil.objects.filter(sede=sede_id)
	all_perfiles = Perfil.objects.filter(sede=sedeId)

	for per in all_perfiles:
		result_set.append((per.legajo,per.usuario.get_full_name))
	return result_set

def getEmpleados(request):
    sede_id = str(request.GET.get('sede_id','CEN'))
    #print(sede_id)
    perfiles = Perfil.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    if sede_id:
        perfiles = Perfil.objects.filter(sede=sede_id)   
    for perfil in perfiles:
        options += '<option value="%s">%s</option>' % (
            perfil.legajo,
            perfil.usuario.get_full_name()
        )
    response = {}
    response['empleados'] = options
    return JsonResponse(response)
def getifxEmpleados(request):
    sede_id = str(request.GET.get('sede_id','CEN'))
    #print(sede_id)
    # perfiles = []
    options = '<option value="" selected="selected">---------</option>'
    if sede_id:
        empleados = ifxEmpleados(pSede=sede_id)   
        # print(perfiles)
    for empleado in empleados:
        options += '<option value="%s">%s</option>' % (
            empleado['legajo'],
            empleado['full_name']
            # perfil.usuario.full_name
            
        )
        # print(p)
    response = {}
    response['empleados'] = options
    return JsonResponse(response)

def ifxEmpleados(**Kwargs):
		####################################################################  
		#IFXPY NECESITA QUE ESTEN DEFINIDOS LOS CLIENTES INFORMIX CLIENT SDK
		####################################################################
		#CENTRAL
		IFX_CEN_HOST = '10.130.10.250'
		IFX_CEN_SERVER = 'ol_informix1170'
		IFX_CEN_SERVICE = '22767'
		IFX_CEN_DB = 'pl4sjasu'
		#VILLETA
		IFX_VTA_HOST = '192.100.100.8'
		IFX_VTA_SERVER = 'ol_platino'
		IFX_VTA_SERVICE = '1530'
		IFX_VTA_DB = 'pl4sjpvi'
		#VALLEMI
		IFX_VMI_HOST = '192.168.100.7'
		IFX_VMI_SERVER = 'ol_informix1171'
		IFX_VMI_SERVICE = '22767'
		IFX_VMI_DB = 'pl4sjvalle'
		

		#CONEXION DEFAULT
		IFX_HOST = IFX_CEN_HOST
		IFX_SERVER = IFX_CEN_SERVER
		IFX_SERVICE = IFX_CEN_SERVICE
		IFX_DB = IFX_CEN_DB
		#COMUN
		IFX_USER = 'informix'
		IFX_PASS ='cnumtc'

		vSede = Kwargs['pSede']
				
		if vSede == 'VTA':
			#CONEXION VILLETA
			IFX_HOST = IFX_VTA_HOST
			IFX_SERVER = IFX_VTA_SERVER
			IFX_SERVICE = IFX_VTA_SERVICE
			IFX_DB = IFX_VTA_DB        
		elif vSede == 'VMI':
			#CONEXION VALLEMI
			IFX_HOST = IFX_VMI_HOST
			IFX_SERVER = IFX_VMI_SERVER
			IFX_SERVICE = IFX_VMI_SERVICE
			IFX_DB = IFX_VMI_DB        
				
		#CADENA DE CONEXION
		ConStr = "SERVER=%s;DATABASE=%s;HOST=%s;SERVICE=%s;UID=%s;PWD=%s;" % (IFX_SERVER,IFX_DB,IFX_HOST,IFX_SERVICE,IFX_USER,IFX_PASS)
		#print(ConStr)
		try:
				# netstat -a | findstr  9088
				conn = IfxPy.connect( ConStr, "", "")
		except Exception as e:
				print ('ERROR: Falla de conexion INFORMIX')
				print ( e )
				quit()
		
		
		  
		#CONSULTA SQL 
		sql = """
				SELECT trim(s.lega) AS legajo, trim(s.nomb) ||' '|| trim(s.apel)||' ['||trim(s.lega)||']'AS full_name
				FROM sjsit s
				ORDER BY 2
				ASC
			  """.format(**Kwargs)
							

		stmt = IfxPy.exec_immediate(conn, sql)
		dic = IfxPy.fetch_assoc(stmt)
		#print(dictionary)
		lista = []
		while dic != False:
				lista.append(dic)        
				dic = IfxPy.fetch_assoc(stmt)
		# print(lista)
		return lista