import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

from cm.models import Paciente
from cm.forms import PacienteForm

class PacienteListView(PermissionRequiredMixin, ListView):
    model = Paciente
    template_name = 'cm/paciente/list.html'
    permission_required = 'cm.view_paciente'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('paciente_create')
        context['title'] = 'Listado de Pacientes'
        return context


class PacienteCreateView(PermissionRequiredMixin, CreateView):
    model = Paciente
    template_name = 'cm/paciente/create.html'
    form_class = PacienteForm
    success_url = reverse_lazy('paciente_list')
    permission_required = 'cm.add_paciente'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()            
            if type == 'denominacion':                
                if Paciente.objects.filter(denominacion__iexact=obj):
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
                data['error'] = 'No ha seleccionado ninguna opci??n'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Paciente'
        context['action'] = 'add'
        return context


class PacienteUpdateView(PermissionRequiredMixin, UpdateView):
    model = Paciente
    template_name = 'cm/paciente/create.html'
    form_class = PacienteForm
    success_url = reverse_lazy('paciente_list')
    permission_required = 'cm.change_paciente'

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
                if Paciente.objects.filter(denominacion__iexact=obj).exclude(id=id):
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
                data['error'] = 'No ha seleccionado ninguna opci??n'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edici??n de un Paciente'
        context['action'] = 'edit'
        return context


class PacienteDeleteView(PermissionRequiredMixin, DeleteView):
    model = Paciente
    template_name = 'cm/paciente/delete.html'
    success_url = reverse_lazy('paciente_list')
    permission_required = 'cm.delete_paciente'

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
        context['title'] = 'Notificaci??n de eliminaci??n'
        context['list_url'] = self.success_url
        return context