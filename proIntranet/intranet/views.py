import pyodbc
import IfxPy
from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
"""
https://simpleisbetterthancomplex.com/tutorial/2016/08/08/how-to-export-to-pdf.html
bajar GTK descomprimir en C:\\msys2\\mingw64
https://weasyprint.readthedocs.io/en/latest/install.html#step-5-run-weasyprint
"""

from bs.utils import * #created in step 4
from .models import *

from .forms import *

from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView 
from django.views.generic.edit import (CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import PermissionRequiredMixin


####################################################################  
#IFXPY NECESITA QUE ESTEN DEFINIDOS LOS CLIENTES INFORMIX CLIENT SDK
####################################################################
#CENTRAL
IFX_CEN_HOST = '10.130.10.250'
IFX_CEN_SERVER = 'ol_informix1170'
IFX_CEN_SERVICE = '22767'
IFX_CEN_DB = 'pl4sjasu'
#VILLETA
IFX_VTA_HOST = '192.100.100.8'
IFX_VTA_SERVER = 'ol_platino'
IFX_VTA_SERVICE = '1530'
IFX_VTA_DB = 'pl4sjpvi'
#VALLEMI
IFX_VMI_HOST = '192.168.100.7'
IFX_VMI_SERVER = 'ol_informix1171'
IFX_VMI_SERVICE = '22767'
IFX_VMI_DB = 'pl4sjvalle'

#############################################
#             PUBLICACIONES
#############################################

class PublicacionList(ListView):
  model = Publicacion
  def get_context_data(self, **kwargs):
      # Call the base implementation first to get a context
      context = super().get_context_data(**kwargs)
      # Add in a QuerySet of all the books
      context['pub_cumple_list'] = Publicacion.objects.filter(cumpleanho=True).order_by('-fecha')[:9]
      return context
  def get_queryset(self):
        # return Publicacion.objects.exclude(imagen='').order_by('-fecha')[:20]
        return Publicacion.objects.filter(cumpleanho=False).order_by('-fecha')[:30]

class PublicacionDetail(DetailView):
  model = Publicacion

class PublicacionCreate(PermissionRequiredMixin,CreateView):
  permission_required = 'intranet.add_publicacion'
  model = Publicacion
  form_class = PublicacionForm
  success_url = reverse_lazy('publicacion:list')
  #fields = '__all__'

class PublicacionUpdate(PermissionRequiredMixin,UpdateView):
  permission_required = 'intranet.change_publicacion'
  model = Publicacion
  success_url = reverse_lazy('publicacion:list')
  fields = '__all__'

class PublicacionDelete(PermissionRequiredMixin,DeleteView):
  permission_required = 'intranet.delete_publicacion'
  model = Publicacion
  success_url = reverse_lazy('publicacion:list')
  #fields = __all__

#############################################
#      CARGAR RECIBOS
#############################################
def recibo(**Kwargs):
  vMes = Kwargs['pMes']
  vAnho = Kwargs['pAnho']
 
  if not (vMes== '02' and vAnho == '2021'):
    return cargarRecibo(**Kwargs)
  else:

    lista=[{"mensaje":"CONSULTA DE RECIBO NO DISPONIBLE POR EL MOMENTO"}]
    return lista
  
#############################################
#     CARGAR ASISTENCIAS 
#############################################
def asistencia(**Kwargs):
  vSede = Kwargs['pSede']
  #print(vSede)
  if (vSede=='VMI'):     
    return cargarAsistenciaVallemi(**Kwargs)
  else:
    return cargarAsistencia(**Kwargs)


def ver_recibo2(request):
    return render(
        request=request,
        template_name='pdf/recibo_pdf.html',
    )
    
@login_required
def ver_recibo(request):
    """Sign up view."""
    usuario = None
    if request.method == 'POST':
        form = pReciboForm(request.POST) 
        if form.is_valid():
            data = form.cleaned_data
            #print(data)
            result=[]
            can_select_empleado = request.user.has_perm('can_select_empleado')
            #CONTROLAR QUE SOLO LOS USUARIOS CON PERMISO PUEDAN CONSULTAR OTROS RECIBOS
            #
            if not can_select_empleado and data['pLegajo']!= str(request.user.perfil.legajo):
                result = [{'mensaje':'Permisos Insuficientes para consultar otros recibos'}]
            else:    
                result = recibo(**data)
                # persona = getIdentificaciones(vCedula=3588321)
                # print(persona)
                #print(form)
                # render_to_response con context_instance is deprecated in django 1.8
                # return render_to_response('pdf/recibo_pdf.html',{'recibos':result},context_instance=RequestContext(request))
            return render(
                request=request,
                template_name='pdf/recibo_pdf.html',
                context={'recibos':result})
    else:
        form = pReciboForm()
        usuario = {'sede':str(request.user.perfil.sede),'cedula':request.user.username, 'legajo':str(request.user.perfil.legajo)}
        #User.objects.filter(username=request.user.username)
        
    return render(
        request=request,
        template_name='ver_recibo.html',
        context={'form': form, 'usuario':usuario}
    )
@login_required
def ver_asistencia(request):
    """Sign up view."""
    usuario = None
    if request.method == 'POST':
        form = pAsistenciaForm(request.POST) 
        if form.is_valid():
            data = form.cleaned_data
            result=[]
            can_select_empleado = request.user.has_perm('auth.can_select_empleado')
            #CONTROLAR QUE SOLO LOS USUARIOS CON PERMISO PUEDAN CONSULTAR OTRAS ASISTENCIAS
            if not can_select_empleado and data['pLegajo']!= str(request.user.perfil.legajo):
                result = [{'mensaje':'Permisos Insuficientes para consultar otras asistencias'}]
            else:    
                result = asistencia(**data)
            #print(result)
            # return render_to_response('pdf/asistencia_pdf.html',{'asistencias':result, 'data':data})
            vTemplateName = 'pdf/asistencia_pdf.html'
            if (data['pSede']=='VMI'):
              vTemplateName = 'pdf/asistencia_pdf_vmi.html'

            return render(
              request=request,
              template_name=vTemplateName,
              context={'asistencias':result, 'data':data})
    else:
        form = pAsistenciaForm()
        usuario = {'sede':str(request.user.perfil.sede),'cedula':request.user.username, 'legajo':str(request.user.perfil.legajo)}
    return render(
        request=request,
        template_name='ver_asistencia.html',
        context={'form': form,'usuario':usuario}
    )    



# def html_to_pdf_view(url):
#     pass

#     from selenium import webdriver
#     import time
#     import os
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     driver = webdriver.Chrome('c://chromedriver//chromedriver.exe')  # Optional argument, if not specified will search path.
#     #driver.get('http://www.google.com/xhtml');

#     #driver = webdriver.PhantomJS("C://phantomjs-2.1.1-windows//bin//phantomjs.exe")
#    # data = recibo(pCedula='3248983',pMes='7',pAnho='2019',pLegajo='3074')
#     #driver.get('http://130.10.10.97:8000/ver_recibo2/')
#     driver.get(url)
#     #html_source = driver.page_source 
#     #html_source = driver.page_source 
#     #html_source = driver.execute_script("return document.documentElement.outerHTML")
#     env = Environment(loader=FileSystemLoader('.'))
#     template = env.get_template("pdf/asistencia_pdf.html")
#     template_vars = {'asistencias':result, 'data':data}
#     html_out = template.render(template_vars)
        
#     #print(html)
#    # data = recibo(pCedula='4647857',pMes='7',pAnho='2019')
#    # html_string = render_to_string('pdf/recibo_pdf.html', {"recibos":data,})
#     html = HTML(string = html_source)
#     css = BASE_DIR+"/static/vendor/fontawesome-free/css/all.min.css"
#     css2 = BASE_DIR+"/static/vendor/datatables/dataTables.bootstrap4.css"
#     css3 = BASE_DIR+"/static/css/sb-admin.css"

#     css  = CSS(filename=css)
#     css2 = CSS(filename=css2)
#     css3 = CSS(filename=css3)
#     filename = '/tmp/mypdf.pdf'

#     #html.write_pdf(filename, stylesheets=[css, "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"])
#     html.write_pdf(filename, stylesheets=[css,css2,css3])

#     fs = FileSystemStorage('/tmp')
#     with fs.open('mypdf.pdf') as pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
#         return response

#     return response

# def myview(request):
#     #Retrieve data or whatever you need
#     return render_to_pdf(
#             'pdf/asistencia_pdf.html',
#             {
#                 'pagesize':'A4',
#                 'mylist': results,
#             }
#         )



# def ver_asistencia_pdf(request):
#     """Sign up view."""
#     usuario = None
#     if request.method == 'POST':
#         form = pAsistenciaForm(request.POST) 
#         if form.is_valid():
#             data = form.cleaned_data
#             print(data)
#             results = asistencia(**data)
#             #print(result)
#             #return 

            
#             env = Environment(loader=FileSystemLoader(settings.TEMPLATES[0].get('DIRS')))
#             print(settings.TEMPLATES[0].get('DIRS'))
            
#             template = env.get_template("pdf/asistencia_pdf.html")
#             template_vars = {'asistencias':result, 'data':data}
#             html_out = template.render(template_vars)
    
#             #print(html)
#             # data = recibo(pCedula='4647857',pMes='7',pAnho='2019')
#             # html_string = render_to_string('pdf/recibo_pdf.html', {"recibos":data,})
#             html = HTML(string = html_out)
#             css = BASE_DIR+"/static/vendor/fontawesome-free/css/all.min.css"
#             css2 = BASE_DIR+"/static/vendor/datatables/dataTables.bootstrap4.css"
#             css3 = BASE_DIR+"/static/css/sb-admin.css"
#             css  = CSS(filename=css)
#             css2 = CSS(filename=css2)
#             css3 = CSS(filename=css3)
#             filename = '/tmp/mypdf.pdf'
            
    
#             #html.write_pdf(filename, stylesheets=[css, "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"])
#             html.write_pdf(filename, stylesheets=[css,css2,css3])

#             fs = FileSystemStorage('/tmp')
#             with fs.open('mypdf.pdf') as pdf:
#                 response = HttpResponse(pdf, content_type='application/pdf')
#                 response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
#             return response

#         return response
  
#     else:
#         form = pAsistenciaForm()
#         usuario = {'sede':str(request.user.perfil.sede),'cedula':request.user.username, 'legajo':str(request.user.perfil.legajo)}
#     return render(
#         request=request,
#         template_name='ver_asistencia.html',
#         context={'form': form,'usuario':usuario}
#     )


###########################################
#      CARGAR ASISTENCIA DE VALLEMI 
###########################################
def cargarAsistenciaVallemi(**Kwargs):
  #PARAMETROS DE CONEXION SQLSERVER VALLEMI
  MSSQL_VMI_SERVER = '192.168.100.48'
  MSSQL_VMI_DB ='db_inc'

  MSSQL_DRIVER = 'ODBC Driver 17 for SQL Server'
  MSSQL_SERVER = MSSQL_VMI_SERVER 
  MSSQL_DB = MSSQL_VMI_DB
  MSSQL_USER='intranet'
  MSSQL_PASS='tic2019*'

  #CADENA DE CONEXION
  ConStr = "DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s;" % (MSSQL_DRIVER,MSSQL_SERVER,MSSQL_DB,MSSQL_USER,MSSQL_PASS)
  #print(ConStr)
  try:
    conn = pyodbc.connect(ConStr)

    cursor = conn.cursor()
    vSql = """SELECT 'VMI' AS sede,
    e.legajo AS lega,
    e.nombre AS nomb,
    e.apellido AS apel,
    t.fecha AS fec_emision,
    t.dia_semana, t.tipo_turno AS turn,
    t.e1 AS hora_entr,
    t.s1 AS hora_sali,
    CONVERT(DECIMAL(5,2),REPLACE(CONVERT(CHAR(5), CONVERT(DATETIME,t.s1) - CONVERT(DATETIME, t.e1), 108),':','.')) AS hora_trab,
    t.e2 AS hora_entr2,
    t.s2 AS hora_sali2,
    CONVERT(DECIMAL(5,2),REPLACE(CONVERT(CHAR(5), CONVERT(DATETIME,t.s2) - CONVERT(DATETIME, t.e2), 108),':','.')) AS hora_trab2,
    t.permiso_motiv AS moti_ause,
    t.hs_permiso AS hora_perm,
    SUBSTRING(t.dia_semana,1,2) AS ccos

    FROM t_rh_tarjeta_n t
    INNER JOIN t_rh_empleado e ON t.id_empleado=e.id_empleado
    WHERE 1=1
    AND e.legajo = {pLegajo}
    AND t.fecha >='{pFechaDesde}'
    AND t.fecha <='{pFechaHasta}'
    ORDER BY t.fecha
    """.format(**Kwargs)
    #print(vSql)
    cursor.execute(vSql)
  except Exception as e:
    print ('ERROR: Connect failed MSSQL SERVER')
    print ( e )
    quit()
      
  # single_row = dict(list(zip(list(zip(*cursor.description))[0], cursor.fetchone())))
  rows = [dict(list(zip(list(zip(*cursor.description))[0], row))) for row in cursor.fetchall()]   
  return rows
#########################################
# CARGA DE ASISTENCIA CENTRAL Y VILLETA 
#########################################
def cargarAsistencia(**Kwargs):
  vSede = Kwargs['pSede']
  #CONEXION DEFAULT
  IFX_HOST = IFX_CEN_HOST
  IFX_SERVER = IFX_CEN_SERVER
  IFX_SERVICE = IFX_CEN_SERVICE
  IFX_DB = IFX_CEN_DB
  #COMUN
  IFX_USER = 'informix'
  IFX_PASS ='cnumtc'

  if vSede == 'VTA':
    #CONEXION VILLETA
    IFX_HOST = IFX_VTA_HOST
    IFX_SERVER = IFX_VTA_SERVER
    IFX_SERVICE = IFX_VTA_SERVICE
    IFX_DB = IFX_VTA_DB        
      
  #CADENA DE CONEXION
  ConStr = "SERVER=%s;DATABASE=%s;HOST=%s;SERVICE=%s;UID=%s;PWD=%s;" % (IFX_SERVER,IFX_DB,IFX_HOST,IFX_SERVICE,IFX_USER,IFX_PASS)
  #print(ConStr)
  try:
      # netstat -a | findstr  9088
      conn = IfxPy.connect( ConStr, "", "")
  except Exception as e:
      print ('ERROR: Falla de conexion INFORMIX')
      print ( e )
      quit()

  # Select records
  sql = """
      SELECT  ashst.ddma_emis  as fec_emision,
              ((CASE WHEN LEN(TRIM(ashst.hora_sali)) > 0 THEN 
                         TO_DATE(ashst.hora_sali,"%Y-%m-%d %H:%M") 
                    ELSE NULL END -
              (CASE WHEN LEN(TRIM(ashst.hora_entr)) > 0 THEN 
                         TO_DATE(ashst.hora_entr,"%Y-%m-%d %H:%M") 
                    ELSE NULL END
              ))::INTERVAL SECOND(6) TO SECOND)::VARCHAR(12)::INT/3600 as hora_trab,                      
              sjsit.lega, sjsit.nomb, sjsit.apel, sjsit.divi, 
              sjsit.depa, sjsit.secc, sjsit.foli, sjsit.foli_baja, 
              ashst.lega, ashst.hora_tipo, ashst.turn, ashst.ddma_emis, 
              CASE WHEN LEN(TRIM(ashst.hora_entr)) > 0 THEN 
                        TO_DATE(ashst.hora_entr,"%Y-%m-%d %H:%M") 
                   ELSE NULL 
               END AS hora_entr,
              CASE WHEN LEN(TRIM(ashst.hora_sali)) > 0 THEN 
                        TO_DATE(ashst.hora_sali,"%Y-%m-%d %H:%M") 
                   ELSE NULL 
               END AS hora_sali,
              ashst.tipo_entr, 
              ashst.ccos as ccos2, sjdiv.nomb_divi, sjdpt.nomb_depa, 
              sjsec.nomb_secc, ashot.nomb_hora_tipo, 
              astur.hora_ent1, astur.hora_sal1, pscco.nomb_ccos,
              ashst.conl,ashst.moti_ause,
              CASE WEEKDAY(ashst.ddma_emis) 
                    WHEN 0 THEN 'Do' 
                    WHEN 1 THEN 'Lu' 
                    WHEN 2 THEN 'Ma' 
                    WHEN 3 THEN 'Mi' 
                    WHEN 4 THEN 'Ju'
                    WHEN 5 THEN 'Vi'
                    WHEN 6 THEN 'Sá'
              ELSE '..'    
              END as ccos
        FROM  sjsit, OUTER(sjdiv), OUTER(sjdpt), OUTER(sjsec), 
              ashst, ashot, OUTER(astur), OUTER pscco , OUTER(sjcol), 
              sjpag, sjdoc 
       WHERE 1 = 1
         and ashst.lega = {pLegajo} 
         
         and ashst.ddma_emis >=TO_DATE("{pFechaDesde}","%Y-%m-%d")
         and ashst.ddma_emis <=TO_DATE("{pFechaHasta}","%Y-%m-%d")
         and sjdoc.lega = ashst.lega
         and sjsit.lega = ashst.lega 
         and sjsit.divi = sjdiv.divi 
         and sjsit.depa = sjdpt.depa 
         and sjsit.secc = sjsec.secc 
         and sjsit.cent_pago = sjpag.cent_pago 
         and sjsit.foli = sjsit.foli_baja 
         and ashst.hora_tipo = ashot.hora_tipo 
         and ashst.turn = astur.turn 
         and ashst.ccos = pscco.ccos 
         and ashst.foli = ashst.foli_baja 
         and ashst.conl = sjcol.conl
         ORDER BY 1 
  """.format(**Kwargs)
          #.format(Kwargs['pCedula'],Kwargs['pLegajo'],Kwargs['pMes'],Kwargs['pAnho'])
  #print(sql)

  stmt = IfxPy.exec_immediate(conn, sql)
  dic = IfxPy.fetch_assoc(stmt)
  #print(dic)
  lista = []
  while dic != False:
      lista.append(dic)        
      dic = IfxPy.fetch_assoc(stmt)
  # print(lista)
  return lista

###########################################
# CARGAR RECIBO CENTRAL, VILLETA, VALLEMI
###########################################
def cargarRecibo(**Kwargs):
    #CONEXION DEFAULT
    IFX_HOST = IFX_CEN_HOST
    IFX_SERVER = IFX_CEN_SERVER
    IFX_SERVICE = IFX_CEN_SERVICE
    IFX_DB = IFX_CEN_DB
    #COMUN
    IFX_USER = 'informix'
    IFX_PASS ='cnumtc'

    vSede = Kwargs['pSede']
        
    if vSede == 'VTA':
      #CONEXION VILLETA
      IFX_HOST = IFX_VTA_HOST
      IFX_SERVER = IFX_VTA_SERVER
      IFX_SERVICE = IFX_VTA_SERVICE
      IFX_DB = IFX_VTA_DB        
    elif vSede == 'VMI':
      #CONEXION VALLEMI
      IFX_HOST = IFX_VMI_HOST
      IFX_SERVER = IFX_VMI_SERVER
      IFX_SERVICE = IFX_VMI_SERVICE
      IFX_DB = IFX_VMI_DB        
        
    #CADENA DE CONEXION
    ConStr = "SERVER=%s;DATABASE=%s;HOST=%s;SERVICE=%s;UID=%s;PWD=%s;" % (IFX_SERVER,IFX_DB,IFX_HOST,IFX_SERVICE,IFX_USER,IFX_PASS)
    #print(ConStr)
    try:
        # netstat -a | findstr  9088
        conn = IfxPy.connect( ConStr, "", "")
    except Exception as e:
        print ('ERROR: Falla de conexion INFORMIX')
        print ( e )
        quit()
    
    #TIPO DE RECIBO
    vTipo = Kwargs['pTipo']
    sql=''
    if vTipo in ('NOR','AGU'):     
      #CONSULTA SQL 
      sql = """
                SELECT * ,
                TO_CHAR(sjhst.ddma_emis,'%d/%m/%Y') as fecha, 
                fnc_nombre_mes(mmes)                as nombre_mes 
                FROM
                sjdoc, sjhst, sjsit, sjcol, sjdiv, outer(sjdpt), outer(sjsec), 
                pscon, sjtem, pscco, sjpag, outer(sjsba), outer(sjcar) 
                where 1 = 1
                AND sjdoc.lega = sjhst.lega                 
                AND sjhst.lega = {pLegajo}
                AND sjhst.mmes = {pMes}
                AND sjhst.aano = {pAnho}
                and sjhst.lega = sjsit.lega and sjhst.conl = sjcol.conl 
                and sjhst.ccos = pscco.ccos and sjhst.conc = pscon.conc 
                and sjsit.tipo_empl = sjtem.tipo_empl 
                and sjsit.divi = sjdiv.divi and sjsit.depa = sjdpt.depa 
                and sjsit.secc = sjsec.secc and sjsit.cent_pago = sjpag.cent_pago 
                and sjsit.carg = sjcar.carg and pscon.tipo = '{pTipo}'
                and sjcol.patr_empl = 'E' and sjsit.foli = sjsit.foli_baja 
                and sjsit.lega = sjsba.lega and sjsit.mone = sjsba.mone 
                and sjsba.ddma_vige = (SELECT max(ddma_vige) 
                                       FROM sjsba b 
                                       WHERE b.lega = sjsba.lega 
                                       AND b.ddma_vige <= sjhst.ddma_emis) 
                and sjhst.foli = sjhst.foli_baja
                and sjhst.conl not in (select conc from sjcoc)
                and sjhst.conl not in (select conl from sjcoc)
                order by sjhst.lega ASC, sjhst.conl ASC, sjhst.dbcr ASC
            """.format(**Kwargs)
              #.format(Kwargs['pCedula'],Kwargs['pLegajo'],Kwargs['pMes'],Kwargs['pAnho'])
        #print(sql)
    #AGUINALDO PRELIMINAR 
    elif vTipo =='AGU2':
      sql = """select * ,
          TO_CHAR(sjliq_tmp.ddma_emis,'%d/%m/%Y') as fecha, 
          fnc_nombre_mes(mmes)                as nombre_mes 
          FROM
          sjdoc, sjliq_tmp, sjsit, sjcol, sjdiv, outer(sjdpt), outer(sjsec), 
          pscon, sjtem, pscco, sjpag, outer(sjsba), outer(sjcar) 
          where 1 = 1
          AND sjdoc.lega = sjliq_tmp.lega 

          AND sjliq_tmp.lega = {pLegajo}
          AND sjliq_tmp.mmes = {pMes}
          AND sjliq_tmp.aano = {pAnho}
          AND sjcol.conl = 211 --{pTipo}
          and sjliq_tmp.lega = sjsit.lega and sjliq_tmp.conl = sjcol.conl 
          and sjliq_tmp.ccos = pscco.ccos and 'LIQ' = pscon.conc 
          and sjsit.tipo_empl = sjtem.tipo_empl 
          and sjsit.divi = sjdiv.divi and sjsit.depa = sjdpt.depa 
          and sjsit.secc = sjsec.secc and sjsit.cent_pago = sjpag.cent_pago 
          and sjsit.carg = sjcar.carg and pscon.tipo = 'NOR'
          and sjcol.patr_empl = 'E' and sjsit.foli = sjsit.foli_baja 
          and sjsit.lega = sjsba.lega and sjsit.mone = sjsba.mone 
          and sjsba.ddma_vige = ( SELECT max(ddma_vige) 
          FROM sjsba b 
          WHERE b.lega = sjsba.lega 
          AND b.ddma_vige <= sjliq_tmp.ddma_emis) 
          --and sjliq_tmp.foli = sjliq_tmp.foli_baja
          order by sjliq_tmp.lega ASC, sjliq_tmp.conl ASC, sjliq_tmp.dbcr ASC
          """.format(**Kwargs)
    else:
      sql = """
                select * ,
                TO_CHAR(sjhst.ddma_emis,'%d/%m/%Y') as fecha, 
                fnc_nombre_mes(mmes)                as nombre_mes 
                FROM
                sjdoc, sjhst, sjsit, sjcol, sjdiv, outer(sjdpt), outer(sjsec), 
                pscon, sjtem, pscco, sjpag, outer(sjsba), outer(sjcar) 
                where 1 = 1
                AND sjdoc.lega = sjhst.lega 
                
                AND sjhst.lega = {pLegajo}
                AND sjhst.mmes = {pMes}
                AND sjhst.aano = {pAnho}
                AND sjcol.conl = {pTipo}
                and sjhst.lega = sjsit.lega and sjhst.conl = sjcol.conl 
                and sjhst.ccos = pscco.ccos and sjhst.conc = pscon.conc 
                and sjsit.tipo_empl = sjtem.tipo_empl 
                and sjsit.divi = sjdiv.divi and sjsit.depa = sjdpt.depa 
                and sjsit.secc = sjsec.secc and sjsit.cent_pago = sjpag.cent_pago 
                and sjsit.carg = sjcar.carg and pscon.tipo = 'NOR'
                and sjcol.patr_empl = 'E' and sjsit.foli = sjsit.foli_baja 
                and sjsit.lega = sjsba.lega and sjsit.mone = sjsba.mone 
                and sjsba.ddma_vige = ( SELECT max(ddma_vige) 
                            FROM sjsba b 
                            WHERE b.lega = sjsba.lega 
                            AND b.ddma_vige <= sjhst.ddma_emis) 
                and sjhst.foli = sjhst.foli_baja
                
                
                order by sjhst.lega ASC, sjhst.conl ASC, sjhst.dbcr ASC
            """.format(**Kwargs)
              #.format(Kwargs['pCedula'],Kwargs['pLegajo'],Kwargs['pMes'],Kwargs['pAnho'])
    
    # print(sql)
    stmt = IfxPy.exec_immediate(conn, sql)
    dic = IfxPy.fetch_assoc(stmt)
    #print(dictionary)
    lista = []
    while dic != False:
        lista.append(dic)        
        dic = IfxPy.fetch_assoc(stmt)
    #print(lista)
    return lista