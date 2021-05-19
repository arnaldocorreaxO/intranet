from django.forms import *
from django import forms
from bs.forms import *
from .models import *
''' 
=============================
===    MOTIVO CONSULTA    ===
============================= '''
class MotivoConsultaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = MotivoConsulta
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'descripcion': forms.TextInput(attrs={'placeholder': 'Ingrese un Motivo de Consulta'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

'''        
=====================
===    PACIENTE   ===
===================== '''
class PacienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ci'].widget.attrs['autofocus'] = True

    class Meta:
        model = Paciente
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese Nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ingrese Apellido'}),
            'sexo':forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'estado_civil':forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'nacionalidad':forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'fecha_nacimiento': forms.DateInput(format='%d-%m-%Y', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'fecha_nacimiento',
                # 'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#fecha_nacimiento'
            }),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data



'''        
=====================
===    CONSULTA   ===
===================== '''
class ConsultaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].widget.attrs['autofocus'] = True

    class Meta:
        model = Consulta
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'fecha': forms.DateInput(format='%d-%m-%Y', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'fecha',
                'value': datetime.now().strftime('%d/%m/%Y'),
                'data-toggle': 'datetimepicker',
                'data-target': '#fecha'
            }),            
            'hora': forms.TimeInput(format='%H:%M:%S', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'hora',
                'value': datetime.now().strftime('%H:%M:%S'),
                'data-toggle': 'datetimepicker',
                'data-target': '#hora'
            }),            
            'motivo_consulta':forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'paciente':forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data