#Django
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView 
from django.views.generic.edit import (CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse

import json as simplejson

#Excepciones
from django.db.utils import IntegrityError

#Modelos
from django.contrib.auth.models import User
from .models import *
#Forms
from .forms import *


###################
### DEPENDENCIA ###
###################
class DependenciaList(ListView):
  model = Dependencia

class DependenciaDetail(DetailView):
  model = Dependencia
  
class DependenciaCreate(PermissionRequiredMixin,CreateView):
  permission_required = 'rh.add_dependencia'
  model = Dependencia
  form_class = DependenciaForm
  success_url = reverse_lazy('dependencia-list')
  #fields = '__all__'

class DependenciaUpdate(PermissionRequiredMixin,UpdateView):
  permission_required = 'rh.change_dependencia'
  model = Dependencia
  success_url = reverse_lazy('dependencia-list')
  fields = '__all__'

class DependenciaDelete(PermissionRequiredMixin,DeleteView):
  permission_required = 'rh.delete_dependencia'
  model = Dependencia
  success_url = reverse_lazy('dependencia-list')
  #fields = __all__

###################
###    CARGO    ###
###################
class CargoList(ListView):
  model = Cargo
 
class CargoDetail(DetailView):
  model = Cargo

class CargoCreate(PermissionRequiredMixin,CreateView):
  permission_required = 'rh.add_cargo'
  model = Cargo
  form_class = CargoForm
  success_url = reverse_lazy('cargo-list')
  #fields = '__all__'

class CargoUpdate(PermissionRequiredMixin,UpdateView):
  permission_required = 'rh.change_cargo'
  model = Cargo
  success_url = reverse_lazy('cargo-list')
  fields = '__all__'

class CargoDelete(PermissionRequiredMixin,DeleteView):
  permission_required = 'rh.delete_cargo'
  model = Cargo
  success_url = reverse_lazy('cargo-list')
  #fields = __all__

#####################
###   INTERNOS    ###
#####################
class InternoList(ListView):
  model = Interno
  def get_queryset(self):
        return Interno.objects.order_by('extension')

class InternoDetail(DetailView):
  model = Interno

class InternoCreate(PermissionRequiredMixin,CreateView):
  permission_required = 'rh.add_interno'
  model = Interno
  form_class = InternoForm
  success_url = reverse_lazy('interno-list')
  #fields = '__all__'

class InternoUpdate(PermissionRequiredMixin,UpdateView):
  permission_required = 'rh.change_interno'
  model = Interno
  success_url = reverse_lazy('interno-list')
  fields = '__all__'

class InternoDelete(PermissionRequiredMixin,DeleteView):
  permission_required = 'rh.delete_interno'
  model = Interno
  success_url = reverse_lazy('interno-list')
  #fields = __all__

###########################################
# FUNCION QUE RETORNA LAS DEPENDENCIAS
# EN FORMATO JSON
###########################################
def getDependencias(request):
  #country_name = request.POST['country_name']
  # import pdb; pdb.set_trace()
  sede_name = request.GET.get('id_sede','CEN')
  # print ("ajax sede_name ", sede_name)

  result_set = []
  all_sedes = []
  answer = str(sede_name[1:-1])
  # selected_sede = Sede.objects.get(denominacion=answer)
  selected_sede = sede_name
  print ("selected sede name", answer)
  # all_dependencias = selected_sede.city_set.all()
  all_dependencias = Dependencia.objects.filter(sede=sede_name)
  for dep in all_dependencias:
      # print ("dep name", dep.denominacion)
      # print ("dep_id",dep.id)
      result_set.append({'denominacion': dep.denominacion,'id':dep.id})
  return HttpResponse(simplejson.dumps(result_set), content_type='application/json')

#############################################
# FUNCION QUE RETORNA LAS DEPENDENCIAS
#############################################
def load_dependencias(request):
  sede_id = request.GET.get('sede')
  dependencias = Dependencia.objects.filter(sede=sede_id).order_by('denominacion')
  return render(request, 'rh/dependencia_dropdown_list_options.html', {'dependencias': dependencias})


# EJEMPLO
# https://stackoverflow.com/questions/25706639/django-dependent-select
# from django.shortcuts import render
# from map.models import *
# from django.utils import simplejson
# from django.http import HttpResponse

# def index(request):
#     countries = Country.objects.all()
#     print countries
#     return render(request, 'index.html', {'countries': countries})

# def getdetails(request):
#     #country_name = request.POST['country_name']
#     country_name = request.GET['cnt']
#     print "ajax country_name ", country_name

#     result_set = []
#     all_cities = []
#     answer = str(country_name[1:-1])
#     selected_country = Country.objects.get(name=answer)
#     print "selected country name ", selected_country
#     all_cities = selected_country.city_set.all()
#     for city in all_cities:
#         print "city name", city.name
#         result_set.append({'name': city.name})
#     return HttpResponse(simplejson.dumps(result_set), mimetype='application/json',     content_type='application/json')
