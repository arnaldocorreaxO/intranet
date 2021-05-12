
from django.http import HttpResponse
from django.template.loader import get_template

#from io import StringIO
#from six import StringIO as StringIO 
from io import StringIO as StringIO 
from io import BytesIO
#from xhtml2pdf import pisa
from django.template import Context
from cgi import escape


from weasyprint import HTML, CSS
from django.conf import settings

from datetime import datetime,timedelta

#datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
#vAnhoActual = datetime.now().year
vFechaActual = datetime.today().strftime('%d/%m/%Y')

def choiceAnho():
    from datetime import datetime
    vAnhoActual = datetime.now().year
    CHOICE = [(str(x),str(x)) for x in range(vAnhoActual,vAnhoActual - 10,-1)]
    return CHOICE

def choiceMes():
    CHOICE=[
            ('1',"Enero"),
            ('2',"Febrero"),
            ('3',"Marzo"),
            ('4',"Abril"),
            ('5',"Mayo"),
            ('6',"Junio"),
            ('7',"Julio"),
            ('8',"Agosto"),
            ('9',"Setiembre"),
            ('10',"Octubre"),
            ('11',"Noviembre"),
            ('12',"Diciembre"),
            ]
    return CHOICE

def fechaInicial():
  from datetime import datetime, timedelta
  return ((datetime.now() - timedelta(days=datetime.now().day - 1)).strftime('%d/%m/%Y'))

def fechaActual():
  from datetime import datetime
  # today = datetime.today()
  # return datetime.date(year=today.year-1, month=today.month, day=today.day)
  return (datetime.now().strftime('%d/%m/%Y'))

def pMesActual():
  from datetime import datetime
  ahora = datetime.now()
  mes = ahora.month
  return mes
def choiceTipoEmpleado():
    CHOICE = [
        ('PER','PERMANENTE'),
        ('CON','CONTRATADO'),
        ('COM','COMISIONADO'),
        ]
    return CHOICE

def choiceSede():
    CHOICE = [
        ('CEN','CENTRAL'),
        ('VTA','VILLETA'),
        ('VMI','VALLEMI'),
        ]
    return CHOICE

def choiceEstado():
    CHOICE = [
        ('A','ACTIVO'),
        ('I','INACTIVO'),        
        ]
    return CHOICE

def choiceGenero():
    CHOICE = [
        ('M','Masculino'),
        ('F','Femenino'),        
        ]
    return CHOICE    

def choiceEstadoCivil():
    CHOICE = [        
        ('SO','Soltero/a'),        
        ('CA','Casado/a'),
        ('VI','Viudo/a'),        
        ('DI','Divorciado/a'),        
        ('SE','Separado/a'),         
        ('DE','Desconocido/a'),         
        ]
    return CHOICE     

def choiceTipoRecibo():
    CHOICE = [
        ('NOR','SALARIO'),
        ('AGU','AGUINALDO'),
        #('100','SUBSIDIO (100) - GRATIFICACION'),
        #('300','SUBSIDIO (300) - GRATIFICACION'),
        ]
    return CHOICE
    
# def render_to_pdf2(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None


#Este es del ejemplo de ReportLab
# def render_to_pdf(template_src, context_dict):
#     template = get_template(template_src)
#     #context = Context(context_dict)
#     #Context esta en desuso
#     context = context_dict
#     html  = template.render(context)
#     result = StringIO()

#     pdf = pisa.pisaDocument(StringIO(html.encode("ISO-8859-1")), result, encoding='UTF-8')
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return HttpResponse('Ocurrio algun error <pre>%s</pre>' % escape(html))


# def pdf_generation2(template_src,context_dict):
# 	html_template = get_template(template_src)
# 	pdf_file - HTML(string-html_template).write_pdf()
# 	response = HttpResponse(pdf_file, content_type='application/pdf')
# 	response['Content-Disposition'] = "filename='prueba.pdf'"
    # return response

def pdf_generation(template_src,context_dict):
    #html_template = get_template('pdf/recibo_pdf.html')

    template = get_template(template_src)
    context = context_dict
    html_template  = template.render(context)
    pdf_file = HTML(string=html_template).write_pdf(
    	stylesheets=[CSS(settings.STATICFILES_DIRS[0] + '/css/sb-admin.css'),CSS(settings.STATICFILES_DIRS[0] + '/css/sb-admin.css')])
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="recibo.pdf"'
    return response	



# def render_to_pdf3(template_src, context_dict):
#     template = get_template(template_src)
#     #context = Context(context_dict)
#     html  = template.render(context_dict)
#     #result = StringIO.StringIO()
#     result = BytesIO()

#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))