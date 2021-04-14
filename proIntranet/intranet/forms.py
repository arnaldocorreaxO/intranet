"""User forms."""

# Django
from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from datetime import datetime,timedelta

#Models
from .models import Publicacion
#Utils
from proIntranet.utils import *


"""Parametros Formulario Recibo"""
class pReciboForm(forms.Form):
    pSede   = forms.ChoiceField(label='Sede',
                                widget=forms.Select(attrs={'class': 'form-control',
                                                           'data-toggle': 'select'}),
                                choices=choiceSede(), 
                                required=True)

    pLegajo   = forms.CharField(label='Empleado',
                                widget=forms.Select(attrs={'class': 'selectpicker form-control',
                                                           'data-toggle': 'select',
                                                           'data-live-search':'true'}),
                                required=True)

    pTipo   = forms.ChoiceField(label='Tipo',
                                widget=forms.Select(attrs={'class': 'form-control',
                                                           'data-toggle': 'select'}),
                                choices=choiceTipoRecibo(), 
                                required=True)
    pMes    = forms.ChoiceField(label='Mes',
                                widget=forms.Select(attrs={'class': 'form-control',
                                                           'data-toggle': 'select'}),
                                choices=choiceMes(), 
                                required=True,
                                initial=str(pMesActual()))
    pAnho   = forms.ChoiceField(label='Año',
                                #min_length=4,
                                #max_length=4,
                                widget=forms.Select(attrs={'class': 'form-control',
                                                           'data-toggle': 'select'}),
                                choices=choiceAnho(), 
                                required=True)

                                #widget=forms.TextInput(attrs={'class': 'form-control'}))
   
"""Parametros Formulario Asistencia"""
class pAsistenciaForm(forms.Form):
    pSede   = forms.ChoiceField(label='Sede',
                                widget=forms.Select(attrs={'class': 'form-control',
                                                           'data-toggle': 'select'}),
                                choices=choiceSede(), 
                                required=True)
      
    pLegajo   = forms.CharField(label='Empleado',
                                widget=forms.Select(attrs={'class': 'selectpicker form-control',
                                                           'data-toggle': 'select',
                                                           'data-live-search':'true'}),
                                required=True)
    pFechaDesde = forms.DateField(label = 'Desde:', initial= fechaInicial(),widget=DatePickerInput(
                                                                          options={
                                                                              "format": "DD/MM/YYYY",
                                                                              "locale": "es", 

                                                                          }))
    pFechaHasta = forms.DateField(label = 'Hasta:',initial= fechaActual(),widget=DatePickerInput(
                                                                          options={
                                                                              "format": "DD/MM/YYYY",
                                                                              "locale": "es", 

                                                                          }))

class PublicacionForm(forms.ModelForm):
  class Meta:
    model = Publicacion
    fields = ('__all__')
    initial = {'fecha':fechaActual(),}
    widgets = {
    'fecha': DatePickerInput(attrs={'class': 'col-md-2'},
                              options={
                                  "format": "DD/MM/YYYY",
                                  "locale": "es", 

                              }),
      #'titulo':forms.TextInput(attrs={'class': 'form-control',
      #                                'placeholder' : 'Ingrese su número de Cédula'}),
    }
"""
    class Meta:
    model = BookInstance
    fields = ['due_back',]
    labels = { 'due_back': _('Renewal date'), }
    help_texts = { 'due_back': _('Enter a date between now and 4 weeks (default 3).'), }
"""