import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

from cm.models import MotivoConsulta
from cm.forms import MotivoConsultaForm

class MotivoConsultaListView(PermissionRequiredMixin, ListView):
    model = MotivoConsulta
    template_name = 'cm/motivo_consulta/list.html'
    permission_required = 'view_motivoconsulta'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('motivo_consulta_create')
        context['title'] = 'Listado de Motivo Consulta'
        return context


class MotivoConsultaCreateView(PermissionRequiredMixin, CreateView):
    model = MotivoConsulta
    template_name = 'cm/motivo_consulta/create.html'
    form_class = MotivoConsultaForm
    success_url = reverse_lazy('motivo_consulta_list')
    permission_required = 'add_motivoconsulta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()            
            if type == 'denominacion':                
                if MotivoConsulta.objects.filter(denominacion__iexact=obj):
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
        context['title'] = 'Nuevo registro Motivo Consulta'
        context['action'] = 'add'
        return context


class MotivoConsultaUpdateView(PermissionRequiredMixin, UpdateView):
    model = MotivoConsulta
    template_name = 'cm/motivo_consulta/create.html'
    form_class = MotivoConsultaForm
    success_url = reverse_lazy('motivo_consulta_list')
    permission_required = 'change_motivoconsulta'

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
                if MotivoConsulta.objects.filter(denominacion__iexact=obj).exclude(id=id):
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
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de Motivo Consulta'
        context['action'] = 'edit'
        return context


class MotivoConsultaDeleteView(PermissionRequiredMixin, DeleteView):
    model = MotivoConsulta
    template_name = 'cm/motivo_consulta/delete.html'
    success_url = reverse_lazy('motivo_consulta_list')
    permission_required = 'delete_motivoconsulta'

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