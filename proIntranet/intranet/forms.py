"""User forms."""

# Django
from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from datetime import datetime,timedelta

#Models
from .models import Publicacion
#Utils
from bs.utils import *

"""Parametros Formulario Recibo"""
class pReciboForm(forms.Form):
    pSede   = forms.ChoiceField(label='Sede',
                                widget=forms.Select(attrs={'class': 'selectpicker form-control',
                                                           'data-toggle': 'select'}),
                                choices=[], # Lo dejamos vacío inicialmente 
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
                                choices=choiceMes(), # Esta lista es estática, no hay problema
                                required=True,
                                initial=mesActual)
    pAnho   = forms.ChoiceField(label='Año',
                                #min_length=4,
                                #max_length=4,
                                widget=forms.Select(attrs={'class': 'form-control',
                                                           'data-toggle': 'select'}),
                                choices=[], # Lo dejamos vacío inicialmente
                                required=True)
    def __init__(self, *args, **kwargs):
        super(pReciboForm, self).__init__(*args, **kwargs)
         # Cargamos los años dinámicamente cada vez que se crea el form
        self.fields['pAnho'].choices = choiceAnho()
        # Aprovechamos para cargar las sedes también si vienen de DB
        self.fields['pSede'].choices = choiceSede()
        
        # Opcional: Establecer el año actual como inicial dinámicamente
        self.fields['pAnho'].initial = str(datetime.now().year)
        self.fields['pMes'].initial = str(datetime.now().month)

                                #widget=forms.TextInput(attrs={'class': 'form-control'}))
   
"""Parametros Formulario Asistencia"""
class pAsistenciaForm(forms.Form):
    pSede = forms.ChoiceField(
        label='Sede',
        widget=forms.Select(attrs={'class': 'selectpicker form-control', 
                                   'data-toggle': 'select'}),
        choices=[], # Lo dejamos vacío inicialmente
        required=True
    )
    pLegajo = forms.CharField(
        label='Empleado',
        widget=forms.Select(attrs={
            'class': 'selectpicker form-control',
            'data-toggle': 'select',
            'data-live-search': 'true'
        }),
        required=True
    )
    
    pMes = forms.ChoiceField(
        label='Mes',
        choices=choiceMes(), # Esta lista es estática, no hay problema
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    pAnho = forms.ChoiceField(
        label='Año',
        choices=[], # Lo dejamos vacío inicialmente
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super(pAsistenciaForm, self).__init__(*args, **kwargs)
        # Cargamos los años dinámicamente cada vez que se crea el form
        self.fields['pAnho'].choices = choiceAnho()
        # Aprovechamos para cargar las sedes también si vienen de DB
        self.fields['pSede'].choices = choiceSede()
        
        # Opcional: Establecer el año actual como inicial dinámicamente
        self.fields['pAnho'].initial = str(datetime.now().year)
        self.fields['pMes'].initial = str(datetime.now().month)

# class pAsistenciaForm(forms.Form):
#     pSede   = forms.ChoiceField(label='Sede',
#                                 widget=forms.Select(attrs={'class': 'form-control',
#                                                            'data-toggle': 'select'}),
#                                 choices=choiceSede(), 
#                                 required=True)
      
#     pLegajo   = forms.CharField(label='Empleado',
#                                 widget=forms.Select(attrs={'class': 'selectpicker form-control',
#                                                            'data-toggle': 'select',
#                                                            'data-live-search':'true'}),
#                                 required=True)
#     # NUEVOS CAMPOS
#     pMes = forms.ChoiceField(
#         label='Mes',
#         choices=MONTH_CHOICES,
#         initial=datetime.datetime.now().month,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
    
#     pAnio = forms.ChoiceField(
#         label='Año',
#         choices=get_year_choices(),
#         initial=datetime.datetime.now().year,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
    # pFechaDesde = forms.DateField(label = 'Desde:', initial= fechaInicial(),widget=DatePickerInput(
    #                                                                       options={
    #                                                                           "format": "DD/MM/YYYY",
    #                                                                           "locale": "es", 

    #                                                                       }))
    # pFechaHasta = forms.DateField(label = 'Hasta:',initial= fechaActual(),widget=DatePickerInput(
    #                                                                       options={
    #                                                                           "format": "DD/MM/YYYY",
    #                                                                           "locale": "es", 

    #                                                                       }))

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