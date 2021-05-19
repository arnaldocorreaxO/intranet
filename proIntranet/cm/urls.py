from django.urls import path
from cm.views.cm.motivo_consulta.views import *
from cm.views.cm.paciente.views import *
from cm.views.cm.consulta.views import *

urlpatterns = [
    # Motivo Consulta
    path('motivo_consulta', MotivoConsultaListView.as_view(), name='motivo_consulta_list'),
    path('motivo_consulta/add/', MotivoConsultaCreateView.as_view(), name='motivo_consulta_create'),
    path('motivo_consulta/update/<int:pk>/', MotivoConsultaUpdateView.as_view(), name='motivo_consulta_update'),
    path('motivo_consulta/delete/<int:pk>/', MotivoConsultaDeleteView.as_view(), name='motivo_consulta_delete'),
    
    # Paciente
    path('paciente', PacienteListView.as_view(), name='paciente_list'),
    path('paciente/add/', PacienteCreateView.as_view(), name='paciente_create'),
    path('paciente/update/<int:pk>/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('paciente/delete/<int:pk>/', PacienteDeleteView.as_view(), name='paciente_delete'),
    
    # Consulta
    path('consulta', ConsultaListView.as_view(), name='consulta_list'),
    path('consulta/add/', ConsultaCreateView.as_view(), name='consulta_create'),
    path('consulta/update/<int:pk>/', ConsultaUpdateView.as_view(), name='consulta_update'),
    path('consulta/delete/<int:pk>/', ConsultaDeleteView.as_view(), name='consulta_delete'),    

   ]
