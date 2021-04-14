#Django
from django import forms
from django.contrib.auth.models import User
#Models
from usuarios.models import Perfil
from bs.models import Ciudad
from rh.models import Dependencia

from bootstrap_datepicker_plus import DatePickerInput

class UsuarioForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','first_name','last_name','email']


class PerfilForm(forms.ModelForm):
	class Meta:
		model = Perfil
		fields = [
					'sede',
					'legajo',
					'telefono',
					'foto',
					'direccion',
					'tip_empleado',
					'fec_nacimiento',
					'fec_vinculacion',
					'dependencia',
					'cargo',
					'genero',
					'documento_identidad',
					'nacionalidad',
					'departamento',
					'ciudad',
					'estado_civil'

				 ]
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['ciudad'].queryset = Ciudad.objects.none()
		self.fields['dependencia'].queryset = Dependencia.objects.none()

		#CIUDAD FIELD
		if 'departamento' in self.data:
			try:
				departamento_id = int(self.data.get('departamento'))
				self.fields['ciudad'].queryset = Ciudad.objects.filter(departamento_id=departamento_id).order_by('denominacion')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			#Retornamos solo las ciudades pertenecientes al Departamento
			#Sin related_name se usa de la siguiente manera 
			if self.instance.departamento:
				self.fields['ciudad'].queryset = self.instance.departamento.ciudad_set.order_by('denominacion')
			#Con related_name se usa de la siguiente manera teniendo en cuenta que ciudad2 es el related_name
			#self.fields['ciudad'].queryset = self.instance.departamento.ciudad2.order_by('ciudad')
			#pass

		# DEPENDENCIA FIELD
		if 'sede' in self.data:
			try:
				# sede_id = int(self.data.get('sede'))
				sede_id = str(self.data.get('sede'))
				self.fields['dependencia'].queryset = Dependencia.objects.filter(sede=sede_id).order_by('denominacion')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			#Acá el queryset es diferente al de Departamento Ciudad porque Sede es un Choice no una clase			
			self.fields['dependencia'].queryset = Dependencia.objects.filter(sede=self.instance.sede).order_by('denominacion')
			