#Django
from django.shortcuts import render
import json as simplejson

#Models
from .models import *

#Utils
from proIntranet.identificaciones import getIdentificaciones
###########################################
# FUNCION QUE RETORNA LAS CIUDADES
# EN FORMATO JSON
###########################################
def getCiudades(request):
	#country_name = request.POST['country_name']
	# import pdb; pdb.set_trace()
	dpto_id = request.GET.get('id_dpto','1')
	# print ("ajax sede_name ", sede_name)

	result_set = []
	all_ciudad = []
	answer = str(dpto_id[1:-1])
	# selected_sede = Sede.objects.get(denominacion=answer)
	selected_dpto = dpto_id
	print ("selected dpto id", answer)
	# all_dependencias = selected_sede.city_set.all()
	all_ciudades = Ciudad.objects.filter(departamento=dpto_id)
	for ciu in all_ciudades:
			# print ("dep name", dep.denominacion)
			# print ("dep_id",dep.id)
			result_set.append({'denominacion': ciu.denominacion,'id':ciu.id})
	return HttpResponse(simplejson.dumps(result_set), content_type='application/json')

#############################################
# FUNCION QUE RETORNA LAS CIUDADES
# METODO 2
#############################################
def load_ciudades(request):
	departamento_id = request.GET.get('dpto')
	ciudades = Ciudad.objects.filter(departamento_id=departamento_id).order_by('denominacion')
	return render(request, 'bs/ciudad_dropdown_list_options.html', {'ciudades': ciudades})
#############################################
# DATOS DE PERSONA IDENTIFICACIONES
# METODO 2
#############################################
def getPersona(request):
	#import pdb; pdb.set_trace()
	vCi = str(request.GET.get('ci','X'))
	print('*'*10)
	print(vCi)
	persona = getIdentificaciones(vCedula=vCi)
	return HttpResponse(simplejson.dumps(persona), content_type='application/json')