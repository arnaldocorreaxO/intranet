#Django
from django import forms

#Models
from .models import *

#DEPENDENCIA
class DependenciaForm(forms.ModelForm):
	class Meta:
		model = Dependencia
		fields = ('__all__')
		#ver labels no agarra
		labels = {
            "dependencia_padre": "Dependencia Padre",
        }

#CARGO
class CargoForm(forms.ModelForm):
	class Meta:
		model = Cargo
		fields = ('__all__')

#INTERNO
class InternoForm(forms.ModelForm):
	class Meta:
		model = Interno
		fields = ('__all__')