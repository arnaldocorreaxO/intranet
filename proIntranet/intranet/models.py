from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Create your models here.
content_type = ContentType.objects.get_for_model(User)

class Aviso(models.Model):
	fecha = models.DateField()
	titulo = models.CharField(max_length=100)
	mensaje = models.TextField()
	imagen = models.ImageField(
		upload_to = 'intranet/img',
		blank=True,
		null=True
		)
	creacion = models.DateTimeField(auto_now_add=True)
	modificacion = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.titulo


class Publicacion(models.Model):
	""" Publicaciones
		Avisos
		Noticias
	"""
	fecha = models.DateField()
	titulo = models.CharField(max_length=120)
	descripcion = models.CharField(max_length=250)
	contenido = models.TextField()
	url = models.URLField(blank=True,null=False)
	imagen = models.ImageField(
		upload_to='intranet/img/post',
		blank=True,
		null=True
		)	
	cumpleanho = models.BooleanField(verbose_name='Sección Cumpleaños',default=False)
	class Meta:
		# db_table = 'publicacion'
		verbose_name = 'Publicacion'
		verbose_name_plural = 'Publicaciones'


	def __str__(self):
		return self.titulo

class Documento(models.Model):
	publicacion = models.ForeignKey(Publicacion,related_name='fk_publicacion_documento',on_delete=models.CASCADE)
	documento = models.FileField(upload_to='intranet/docs')

	class Meta:
		# db_table = u'documento'
		verbose_name ='Documento'
		verbose_name_plural ='Documentos'