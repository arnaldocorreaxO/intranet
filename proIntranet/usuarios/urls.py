#Django 
from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
	########################
	# USUARIOS
	########################
	# Este login es personalizado utiliza la vista login_view y no el default login de auth django
	path ('login/', views.login_view, name = 'login2'),
	path ('logout/', views.logout_view, name = 'logout'),
	path ('signup/', views.signup_view, name = 'signup'),
	path ('read/<str:usuario_id>/', views.UsuarioPerfilDetail.as_view(), name='perfil-detail'),
	path ('update/', views.UsuarioPerfilUpdate.as_view(), name='perfil-edit'),
	path ('ver_sol_intra/<int:usuario_id>', views.ver_sol_intra, name='ver_sol_intra'),
	path ('loginactivate/', views.activate_view, name = 'activate'),

	#JSON
	path ('ajax/getEmpleados/', views.getEmpleados, name = 'getEmpleados'), #USUARIOS INTRANET
	path ('ajax/getifxEmpleados/', views.getifxEmpleados, name = 'getifxEmpleados'), #EMPLEADOS INFORMIX
	
]