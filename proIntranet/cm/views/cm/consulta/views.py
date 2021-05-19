from datetime import date, datetime
from reports.forms import ReportForm
import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView

from cm.forms import Consulta, ConsultaForm
from django.contrib.auth.mixins import PermissionRequiredMixin



class ConsultaListView(PermissionRequiredMixin, FormView):
    # model = Consulta
    template_name = 'cm/consulta/list.html'
    permission_required = 'view_consulta'
    form_class = ReportForm
 
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                today = date.today()
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                search = Consulta.objects.filter().order_by('fecha','hora')
                if len(start_date) and len(end_date):
                   search = search.filter(fecha__range=[start_date, end_date])
                position = 1
                for i in search:                    
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1

            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('consulta_create')
        context['title'] = 'Listado de Consultas'
        return context


class ConsultaCreateView(PermissionRequiredMixin, CreateView):
    model = Consulta
    template_name = 'cm/consulta/create.html'
    form_class = ConsultaForm
    success_url = reverse_lazy('consulta_list')
    permission_required = 'add_consulta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:            
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()            
            if type == 'denominacion':                
                if Consulta.objects.filter(denominacion__iexact=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de Consulta'
        context['action'] = 'add'
        return context


class ConsultaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Consulta
    template_name = 'cm/consulta/create.html'
    form_class = ConsultaForm
    success_url = reverse_lazy('consulta_list')
    permission_required = 'change_consulta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            id = self.get_object().id
            if type == 'denominacion':
                if Consulta.objects.filter(name__iexact=obj).exclude(id=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            elif action == 'search_manzana_id':
                data = [{'id': '', 'text': '------------'}]
                for i in Manzana.objects.filter(barrio_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.denominacion, 'data': i.barrio.toJSON()})
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un elector'
        context['action'] = 'edit'
        return context


class ConsultaDeleteView(PermissionRequiredMixin, DeleteView):
    model = Consulta
    template_name = 'cm/consulta/delete.html'
    success_url = reverse_lazy('consulta_list')
    permission_required = 'delete_consulta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
