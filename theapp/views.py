from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.template.loader import get_template
from django.template import RequestContext, Context
from django.shortcuts import render_to_response
from models import AllIncidencias, Incidencias, Usuarios, Channel, Incidencias_User, Conf_User

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import string
import urllib2
from django import *
from django.http import *
from django.utils import timezone
from django.contrib.auth import authenticate, logout, login



# Create your views here.

def normalize_whitespace(text):
	"Remove redundant whitespace from a string"
	return string.join(string.split(text), ' ')

class myContentHandler(ContentHandler):

		def __init__ (self):
			self.inItem = False
			self.inTipo = False
			self.thetipo  = ""
			self.inProvincia = False
			self.inMatricula = False
			self.inCausa = False
			self.inAutonomia = False
			self.inSentido = False
			self.inDate = False
			self.inNivel = False
			self.inCarretera = False
			self.inPoblacion = False
			self.inPk_inicial = False
			self.inPk_final = False
			self.inCausa = False
			
			self.thePk_final = ""
			self.thePk_inicial = ""
			self.thePoblacion = ""
			self.theCarretera = ""
			self.theNivel = ""
			self.theDate = ""
			self.theSentido =""
			self.theAutonomia = ""
			self.theCausa = ""
			self.causa =""
			self.theProvincia = ""
			self.titular=""
			self.theTipo = ""
			self.theMatricula = ""
			self.theIncidencia = ""
			self.tipo=[]
			self.causa = []
			self.provincia = []
			self.nivel = []
			self.date = []
			self.autonomia = []
			self.sentido = []
			self.matricula = []
			self.carretera = []
			self.poblacion = []
			self.pk_inicial =[]
			self.pk_final = []
			self.incidencia = []

		def startElement (self, name, attrs):
			if name == 'incidencia':
				self.inItem = True
			elif self.inItem:
				if name == 'tipo':
					self.inTipo = True
				elif name == 'provincia':
					self.inProvincia = True
				elif name == 'causa':
					self.inCausa = True
				
				elif name == 'matricula':
					self.inMatricula = True

				elif name == 'nivel':
					self.inNivel = True
					

				elif name == 'poblacion':
					self.inPoblacion = True

				elif name == 'sentido':
					self.inSentido = True

				elif name == 'carretera':
					self.inCarretera = True

				elif name == 'autonomia':
					self.inAutonomia = True

				
				elif name == 'pk_inicial':
					self.inPk_inicial =True
				   
				elif name == 'pk_final':
					self.inPk_final = True

				elif name == 'fechahora_ini':
					self.inDate = True



		def endElement (self, name):

			if name == 'incidencia':
				#self.incidencia.append(self.theIncidencia)
				self.inItem = False
				#self.theIncidencia = ""
			
			elif self.inItem:
			
				if name == 'tipo':
					
					self.tipo.append(self.theTipo)	# vinculo = <title>hahahah</title>			    
					self.inTipo = False
					self.theTipo = ""
							
					
					
				elif name == 'provincia':
											
					self.provincia.append(self.theProvincia)
					
					self.inProvincia = False
					self.theProvincia = ""
				
				
				elif name == 'causa':
					
					
					self.causa.append(self.theCausa)
					self.inCausa = False
					self.theCausa = ""
		
				elif name == 'matricula':

					self.matricula.append(self.theMatricula)
					self.inMatricula = False
					self.theMatricula = ""

				elif name == 'nivel':
					self.nivel.append(self.theNivel)
					self.inNivel = False
					self.theNivel =""


				
				elif name == 'poblacion':	
					self.poblacion.append(self.thePoblacion)
					self.inPoblacion = False
					self.thePoblacion = ""
				
				elif name == 'carretera':
					self.carretera.append(self.theCarretera)
					self.inCarretera = False
					self.theCarretera =""

				
				
				
				elif name == 'sentido':
					self.sentido.append(self.theSentido)
					self.inSentido = False
					self.theSentido = ""

				elif name == 'autonomia':

					self.autonomia.append(self.theAutonomia)
					self.inAutonomia = False
					self.theAutonomia = ""

				elif name == 'pk_inicial':
					self.pk_inicial.append(self.thePk_inicial)
					self.inPk_inicial = False
					self.thePk_inicial = ""

				elif name == 'pk_final':
					self.pk_final.append(self.thePk_final)
					self.inPk_final = False
					self.thePk_final= ""

				elif name == 'fechahora_ini':
					self.date.append(self.theDate)
					self.inDate = False
					self.theDate = ""


		def characters (self, chars):
			if self.inTipo:
				self.theTipo = self.theTipo + chars
			
			elif self.inProvincia:
				self.theProvincia = self.theProvincia + chars
			
			elif self.inCausa:
				self.theCausa = self.theCausa + chars 
		
			elif self.inMatricula:
				self.theMatricula = self.theMatricula + chars

			elif self.inNivel:
				self.theNivel = self.theNivel + chars

			elif self.inSentido:
				self.theSentido = self.theSentido + chars

			elif self.inCarretera:
				self.theCarretera = self.theCarretera + chars

			

			elif self.inAutonomia:
				self.theAutonomia = self.theAutonomia + chars


			elif self.inPoblacion:
				self.thePoblacion = self.thePoblacion + chars

			elif self.inPk_inicial:
				self.thePk_inicial = self.thePk_inicial + chars

			elif self.inPk_final:
				self.thePk_final = self.thePk_final + chars
			
			elif self.inDate:
				self.theDate = self.theDate + chars

		def tipos (self):
			return self.tipo

		def causas (self):
			return self.causa

		def provincias(self):
			return self.provincia

		def matriculas(self):
			return self.matricula

		def nivels (self):
			self.nivel
			return self.nivel

		def sentidos (self):
			return self.sentido

		def carreteras (self):
			return self.carretera

		def poblacions (self):
			return self.poblacion

		def pk_inicials (self):
			return self.pk_inicial

		def pk_finals (self):
			return self.pk_final

		def fechas (self):
			return self.date

		def autonomias(self):
			return self.autonomia


def principal(request, resource):


	template = get_template("inicio.html")
	#return HttpResponse("<html><p> <title>adultos</title> </p> <body ><p ALIGN = center>LA PAGINA DE INICIO</p> </body></hmtl>")
	return HttpResponse(template.render(Context({})))
	


def procesar (text): # Este metodo quita las comillas y caracteres no deseados de una lista

	reply = text.split("',")
	
	return reply


def ToString(text): # Este metodo recibe una string con el formato lista y quita caracteres no deseados

	lista = text.split("u'")
	return lista[1]





@csrf_exempt
def actualizar(request):

	
	theParser = make_parser()
	theHandler = myContentHandler()
	theParser.setContentHandler(theHandler)
	
	reply = urllib2.urlopen("http://www.dgt.es/incidencias.xml")		

	theParser.parse(reply)
	print "longitud"+ str(len(theHandler.causas()))
	Causas = theHandler.causas()
	Provincias = theHandler.provincias()
	Matriculas = theHandler.matriculas()
	Tipos = theHandler.tipos()
	Sentido = theHandler.sentidos()
	Carretera = theHandler.carreteras()
	Poblacion = theHandler.poblacions()
	Pk_I = theHandler.pk_inicials()
	Pk_F = theHandler.pk_finals()
	Fecha = theHandler.fechas()
	Autonomia = theHandler.autonomias()
	Nivel = theHandler.nivels()
	
	try:
		listt = Channel.objects.get(pk=1)

		listt. Title_Channel = "incidencias_dgt"
		ident = Channel.objects.get(pk=listt.id)
		#pass
	except Channel.DoesNotExist:

		NuevoCanal = Channel(Title_Channel = "incidencias_dgt")
		NuevoCanal.save()
		ident = Channel.objects.get(pk=NuevoCanal.id)
		#pass

	
	try:
			
		
		for i in range(19):
			p = Incidencias.objects.get(pk =i+1)
			p.Tipo = Tipos[i]
			p.Autonomia = Autonomia[i]
			p.Provincia = Provincias[i]
			p.Matricula = Matriculas[i]
			p.Causa = Causas[i]
			p.Poblacion = Poblacion[i]
			p.Fecha = Fecha[i]
			p.Nivel = Nivel[i]
			p.Carretera = Carretera[i]
			p.PK_I = Pk_I[i]
			p.PK_F = Pk_F[i]
			p.Sentido = Sentido[i]
			p.save()
		
		inicio = "<a href='/' target='_self'> <input type='button' name='boton' value='inicio' /> </a> "
		return  HttpResponseRedirect('/incidencias')
	except Incidencias.DoesNotExist:

		for i in range (19):
			inc = ident.incidencias_set.create ( Tipo = Tipos[i], Autonomia = Autonomia[i], Provincia = Provincias[i],Matricula = Matriculas[i], Causa = Causas[i], Poblacion = Poblacion[i], Fecha = Fecha[i], Nivel = Nivel[i], Carretera = Carretera[i], PK_I = Pk_I[i], PK_F = Pk_F[i], Sentido = Sentido[i])
			inc.save()
			#pass
			#Incidencia = incidencias_set.create(Tipo=entry.title,Provincia=entry.link,Carretera=entry.description,Fecha=timezone.now(),id_canal=PutCanal.id)

		return  HttpResponseRedirect('/incidencias')

@csrf_exempt
def page_user(request,user_selec):  # Muestra la pagina del usuario tanto logueado como no logueado
	""" recurso: /usuario  """
	""" con esa funcion devolvemos la interfaz publica o privada del usuario
		dependiendo de si se ha autenticado o no """
	
	 
	
	if request.user.is_authenticated():
		user=request.user.username 
		# verificamos que el verbo es GET
		
		if request.method == "GET":
			try:
				usuario = Usuarios.objects.get(user_name=user_selec)   # coge de la base de datos el usuario que se llame "user" 
				id_user = Usuarios.objects.get(pk=usuario.id)
				incidencias_usuario = id_user.incidencias_user_set.all() # parsea  "lista_noticias" para luego usarlo en el siguiente for, el cual extrae las noticias
				Incidencias_user = ' '
				try:
					name = Conf_User.objects.get(Ident_User=user_selec).Titulo_revista
				except Conf_User.DoesNotExist:
					name = 'Pagina de ' + usuario.user_name
				for objetos in incidencias_usuario:
					
					tipo = " <font size =5 color=blue>tipo de incidencia: "+ objetos.Tipo + "</font>"
					auto = " en la comunidad de "+objetos.Autonomia
					prov = objetos.Provincia
					mat = "matricula " +objetos.Matricula
					cau = "causada por "+objetos.Causa
					pob = objetos.Poblacion
					fech = "publicada en "+objetos.Fecha
					niv = objetos.Nivel
					carr = "Carretera "+objetos.Carretera
					p_i = objetos.PK_I
					p_f = objetos.PK_F
					longitud = " alcance de " + str(abs (float(p_i)-float(p_f)))+ " km"
					sentid = objetos.Sentido 
					
					tipo_incidencias =  " " + tipo + " <br>" + auto + "("+prov + ") <br>"+ carr + " <br>"+ cau +  " <br>"+ pob  + " <br>"+ fech + " <br>"+ niv + " <br>"+ mat+ " <br>"+ longitud +"<br><br>"
					#respuesta+= incide

					#tipo_incidencias=  objetos.Tipo + ' </br> '+objetos.Provincia+ ' '+ objetos.Carretera+'</br>' 
					resto = "" # FALTA COLOCAR LOS DETALLES
					Incidencias_user += tipo_incidencias+ '</br>' + 'publicado en: '+ objetos.Fecha + '</br> elegida en: ' + str(objetos.Date_Create) + '</br>'+ resto + '</br></br>'
					#se guarga en Incidencias_user las noticias de ese usuario              
					#Incidencias_user += '<a href='+'"'+'canales/'+ objetos.enlace_canal + '">' +'canal revista' + '</a></br></br>'
				
				if user == usuario.user_name:
					edit = True
				else:
					edit = False

				template = get_template("user.html")
				rss =  '<ul><li><h2>'+'<a href='+user_selec+'/rss >subscribirse rss'+'</h2></li></ul>'
				link_css= '<link href="'+ user_selec+'/css'+'"'+ 'rel="stylesheet">'
				return HttpResponse(template.render(Context({'edit':edit,'name':name,'Incidencias_user':Incidencias_user,'user':user, 'rss':rss,'link_css':link_css})))

			except Usuarios.DoesNotExist:
				return HttpResponse("USER  NOT EXITS")
		else:
			return HttpResponse("METODO NO DISPONIBLE")

	else:
		try:
			usuario = Usuarios.objects.get(user_name=user_selec)   
			id_user = Usuarios.objects.get(pk=usuario.id)
			incidencias_usuario = id_user.incidencias_user_set.all() 
			Incidencias_user = ' '
			try:
				name = Conf_User.objects.get(Ident_User=user_selec).Titulo_revista
			except Conf_User.DoesNotExist:
				name = 'Pagina de ' + usuario.user_name
			for objetos in incidencias_usuario:
				#Incidencias_user += objetos.Tipo + '</br>' + 'publicado en: '+ str(objetos.Fecha) + ' creado en: ' + str(objetos.Date_Create) + '</br>'+ objetos.Carretera + '</br>'+ '<a href='+'"'+'canales/'+ objetos.enlace_canal + '">' +'canal revista' + '</a></br></br>'
				#tipo_incidencias=  objetos.Tipo + ' </br> '+objetos.Provincia+ ' '+ objetos.Carretera+'</br>' 
				#resto = "" # FALTA COLOCAR LOS DETALLES
				#Incidencias_user += tipo_incidencias+ '</br>' + 'publicado en: '+ objetos.Fecha + ' </br>elegida en: ' + str(objetos.Date_Create) + '</br>'+ resto + '</br></br>'

				tipo = " <font size =5 color=blue>tipo de incidencia: "+ objetos.Tipo + "</font>"
				auto = " en la comunidad de "+objetos.Autonomia
				prov = objetos.Provincia
				mat = "matricula " +objetos.Matricula
				cau = "causada por "+objetos.Causa
				pob = objetos.Poblacion
				fech = "publicada en "+objetos.Fecha
				niv = objetos.Nivel
				carr = "Carretera "+objetos.Carretera
				p_i = objetos.PK_I
				p_f = objetos.PK_F
				longitud = " alcance de " + str(abs (float(p_i)-float(p_f)))+ " km"
				sentid = objetos.Sentido 
					
				tipo_incidencias =  " " + tipo + " <br>" + auto + "("+prov + ") <br>"+ carr + " <br>"+ cau +  " <br>"+ pob  + " <br>"+ fech + " <br>"+ niv + " <br>"+ mat+ " <br>"+ longitud +"<br><br>"
					#respuesta+= incide

					#tipo_incidencias=  objetos.Tipo + ' </br> '+objetos.Provincia+ ' '+ objetos.Carretera+'</br>' 
				resto = "" # FALTA COLOCAR LOS DETALLES
				Incidencias_user += tipo_incidencias+ '</br>' + 'publicado en: '+ objetos.Fecha + '</br> elegida en: ' + str(objetos.Date_Create) + '</br>'+ resto + '</br></br>'
			
			user=None      
			rss =  '<ul><li><h2>'+'<a href='+user_selec+'/rss >subscribirse rss'+'</h2></li></ul>'
			link_css= '<link href="'+ user_selec+'/css'+'"'+ 'rel="stylesheet">'
			template = get_template("user.html")
			return HttpResponse(template.render(Context({'name':name,'Incidencias_user':Incidencias_user,'user':user, 'rss':rss,'link_css':link_css})))
		except Usuarios.DoesNotExist:
			return HttpResponse("USER NOT EXISTS")

	

def listaPaginas():

	
		respuesta = u' '
	     
        #user = request.user.username
        
		
		listado = Conf_User.objects.all()
				
 		for objeto in listado:
			try:
				titulo = objeto.Titulo_revista
			except Conf_User.DoesNotExist:
				
				titulo=  'Pagina de '+objeto.Ident_User 
        	    #respuesta = str(respuesta)
			nombre = objeto.Ident_User
			usuario = Usuarios.objects.get(user_name=nombre) 
			Ident =Usuarios.objects.get(pk=usuario.id)
			incidencias_usuario = Ident.incidencias_user_set.all()
			#ultima_act= str(incidencias_usuario[len(incidencias_usuario)-1].Date_Create)
			respuesta +='<a href='+'"'+objeto.Ident_User+'"'+'>' +  titulo + ' </a> ' +  objeto.Ident_User +  '</font></br>'
            
		return respuesta   



    
@csrf_exempt
def home(request): 
	
	try:
		
		if request.user.is_authenticated():
			user=request.user.username
		else:
			user = None

		refres = "<a href='/update' target='_self'> <input type='button' name='boton' value='Actualizar' /> </a> "
		try:
			id_canal = Channel.objects.get(pk=1)
			
		except Channel.DoesNotExist:

			NuevoCanal = Channel(Title_Channel = "incidencias_dgt")
			NuevoCanal.save()
			id_canal = Channel.objects.get(pk=1)
			
		
		incidencias_canal= id_canal.incidencias_set.all()
		respuesta = " "
		indice =0
		for elements in incidencias_canal:
			
			indice = indice +1
			tipo = " <font size =5 color=blue>tipo de incidencia: "+ elements.Tipo + "</font>"
			auto = " en la comunidad de "+elements.Autonomia
			prov = elements.Provincia
			mat = "matricula " +elements.Matricula
			cau = "causada por "+elements.Causa
			pob = elements.Poblacion
			fech = "publicada en "+elements.Fecha
			niv = elements.Nivel
			carr = "Carretera "+elements.Carretera
			p_i = elements.PK_I
			p_f = elements.PK_F
			longitud = " alcance de " + str(abs (float(p_i)-float(p_f)))+ " km"
			sentid = elements.Sentido 
		
			incide =  " " + tipo + " <br>" + auto + "("+prov + ") <br>"+ carr + " <br>"+ cau +  " <br>"+ pob  + " <br>"+ fech + " <br>"+ niv + " <br>"+ mat+ " <br>"+ longitud +"<br><br>"
			respuesta+= incide


		#print "incide " + incide 
		listado = listaPaginas()
		print "listado " + listado 
		#listado = "usuarios "
		template = get_template("inicio.html")
		return HttpResponse(template.render(Context({'respuesta':respuesta, 'listado':listado, 'user':user})))

	
	except Incidencias.DoesNotExist:

		
		return HttpResponse("<html><body><h1> actualice el canal porfavor</h1></body></html>")     




def add_incidencia(request,id_inc): #Ese metodo implementa cmo el usuario agrega incidencias a su pagina usuario
	   
	   if request.user.is_authenticated():
		   if request.method == 'GET':
			   try:
				   user=request.user.username 
				   print "usuario register "+ user
				   tipo  = Incidencias.objects.get(pk=id_inc).Tipo
				   carretera = Incidencias.objects.get(pk=id_inc).Carretera
				   fecha= Incidencias.objects.get(pk=id_inc).Fecha
				   prov =Incidencias.objects.get(pk=id_inc).Provincia 
				   #id_canal= Incidencias.objects.get(pk=id_inc).id_canal
				   auto =Incidencias.objects.get(pk=id_inc).Autonomia
				   mat =Incidencias.objects.get(pk=id_inc).Matricula 
				   causa =Incidencias.objects.get(pk=id_inc).Causa
				   pob =Incidencias.objects.get(pk=id_inc).Poblacion
				   niv =Incidencias.objects.get(pk=id_inc).Nivel
				   p_i = Incidencias.objects.get(pk=id_inc).PK_I
				   p_f =Incidencias.objects.get(pk=id_inc).PK_F
				   sentido = Incidencias.objects.get(pk=id_inc).Sentido
				   usuario = Usuarios.objects.get(user_name=user)
				   ident = Usuarios.objects.get(pk=usuario.id)
				   incide = ident.incidencias_user_set.create(Tipo=tipo ,Provincia = prov,Carretera=carretera,Fecha=fecha,Date_Create=timezone.now(),Autonomia= auto, Matricula = mat, Causa = causa,Poblacion = pob, Nivel = niv, PK_I = p_i, PK_F = p_f, Sentido = sentido)
				   incide.save()
				   respuesta = 'se ha agregado la incidencia:'+ '</br>' + tipo 
				   #respuesta = None
			   except ValueError:
				   print 'valor erroneo'
		   else:
			   respuesta = 'Metodo no permitido'
	   else:
			respuesta = 'tienes que loguearte <a href="/login">Login</a>'     
	   return HttpResponseRedirect('/incidencias')


def show_incidencias(request): #muestra la pagina de Incidencias de la aplicacion
	
			if request.method == 'GET':
				
				todo = "todo"
			elif request.method == 'POST':
				if request.POST['filtro'] == 'provincia':
					todo = "prov"
				elif request.POST['filtro'] == 'tipo':
					todo = "tipo"
				elif request.POST['filtro'] == 'longitud':
					todo = "len"
				elif request.POST['filtro'] == 'todas':
					todo = "todo"

			if request.user.is_authenticated():
				user=request.user.username
			else:
				user = None


			title = Channel.objects.get(pk=1).Title_Channel # tipo  del canal cuya clave primaria es al especificada
			#enlace = Channel.objects.get(pk=1).Rss # enlace a la pagina original
			#enlace_rss = Channel.objects.get(pk=1).prov_rss # prov al canal rss original
			
			#tipo  ='<ul><li><h3><a href ='+ enlace + ' >'+title+'</a></h3></li></ul>' 
			#canal = '<ul><li><h3><a href ='+ enlace_rss + ' >(canal)</a></h3></li></ul>'
			act_canal = '<ul><li><h3><a href ='+ '/update' + ' > actualizar canal</a></h3></li></ul>'
			Incidencias_canal = ' '
			PorProvincia = ' '
			PorTipo = ' '
			PorLongitud = ' '
			incide = ' '
			indice = 0
			id_canal = Channel.objects.get(pk=1) #"id_canal" guarda la referencia al canal especificado por la clave "1"
			incidencias_canal= id_canal.incidencias_set.all() # "Incidencias_canal" extrae  la lista de notcias del canal correpondiente al identificador "id_canal"
			for elem in incidencias_canal:
				#Titulo_revista= elem.Tipo +  ' Carretera ' +elem.Carretera + ' (' + elem.Provincia + ')' +  '<br> '
				#Incidencias_canal += Titulo_revista + ' '+'<a href ='+ '/incidencias/' +str(elem.id)+ ' >agregar </a></br></br>' # Noticias canal devuelve cada noticia con su tipo , descripcion y un enlace para que el usuario autenticado pueda agregarla
				#Incidencias_canal += Titulo_revista + ' </br>'
				PorProvincia +=  "provincia de "+elem.Provincia + '<br> '
				PorTipo += "tipo: "+elem.Tipo +'<br> ' 
				PorLongitud += str(abs(float(elem.PK_I)-float(elem.PK_F))) +' kilometros <br> ' 
			
				add = '<a href ='+ '/incidencias/' +str(elem.id)+ ' >agregar </a></br></br>'    
				indice = indice +1
				tipo = " <font size =5 color=blue>tipo de incidencia: "+ elem.Tipo + "</font>"+ add
				auto = " en la comunidad de "+elem.Autonomia
				prov = elem.Provincia
				mat = "matricula " +elem.Matricula
				cau = "causada por "+elem.Causa
				pob = elem.Poblacion
				fech = "publicada en "+elem.Fecha
				niv = elem.Nivel
				carr = "Carretera "+elem.Carretera
				p_i = elem.PK_I
				p_f = elem.PK_F
				longitud = " alcance de " + str(abs (float(p_i)-float(p_f)))+ " kilometros"
				sentid = elem.Sentido 
				
				incide =  " " + tipo + " <br>" + auto + "("+prov + ") <br>"+ carr + " <br>"+ cau +  " <br>"+ pob  + " <br>"+ fech + " <br>"+ niv + " <br>"+ mat+ " <br>"+ longitud +"<br>"+ add
				Incidencias_canal+= incide



			if todo == "todo":
				respuesta = Incidencias_canal

			elif todo == "prov":
				respuesta = PorProvincia
			elif todo == "tipo":
				respuesta = PorTipo

			else:
				respuesta = PorLongitud
			
			num = str(indice)
			template = get_template("incidencias.html")
			return HttpResponse(template.render(Context({'num':num,'user':user,'Incidencias_canal':respuesta,'act_canal':act_canal,'todo':todo})))

@csrf_exempt
def show_todas(request): #muestra la pagina de Todas las incidencias
	
			
			if request.method == 'GET':
				
				todo = "todo"
			elif request.method == 'POST':
				if request.POST['filtro'] == 'provincia':
					todo = "prov"
				elif request.POST['filtro'] == 'tipo':
					todo = "tipo"
				elif request.POST['filtro'] == 'longitud':
					todo = "len"
				elif request.POST['filtro'] == 'todas':
					todo = "todo"

			title = Channel.objects.get(pk=1).Title_Channel # tipo  del canal cuya clave primaria es al especificada
			#enlace = Channel.objects.get(pk=1).Rss # enlace a la pagina original
			#enlace_rss = Channel.objects.get(pk=1).prov_rss # prov al canal rss original
			
			#tipo  ='<ul><li><h3><a href ='+ enlace + ' >'+title+'</a></h3></li></ul>' 
			#canal = '<ul><li><h3><a href ='+ enlace_rss + ' >(canal)</a></h3></li></ul>'
			act_canal = '<ul><li><h3><a href ='+ '/update' + ' > actualizar canal</a></h3></li></ul>'
			Incidencias_canal = ' '
			PorProvincia = ' '
			PorTipo = ' '
			PorLongitud = ' '
			incide = ' '
			indice = 0
			id_canal = Channel.objects.get(pk=1) #"id_canal" guarda la referencia al canal especificado por la clave "1"
			incidencias_canal= id_canal.incidencias_set.all() # "Incidencias_canal" extrae  la lista de notcias del canal correpondiente al identificador "id_canal"
			for elem in incidencias_canal:
				#Titulo_revista= elem.Tipo +  ' Carretera ' +elem.Carretera + ' (' + elem.Provincia + ')' +  '<br> '
				#Incidencias_canal += Titulo_revista + ' '+'<a href ='+ '/incidencias/' +str(elem.id)+ ' >agregar </a></br></br>' # Noticias canal devuelve cada noticia con su tipo , descripcion y un enlace para que el usuario autenticado pueda agregarla
				#Incidencias_canal += Titulo_revista + ' </br>'
				PorProvincia +=  "provincia de "+elem.Provincia + '<br> '
				PorTipo += "tipo: "+elem.Tipo +'<br> ' 
				PorLongitud += str(abs(float(elem.PK_I)-float(elem.PK_F))) +' kilometros <br> ' 
			
			    
				indice = indice +1
				tipo = " <font size =5 color=blue>tipo de incidencia: "+ elem.Tipo + "</font>"
				auto = " en la comunidad de "+elem.Autonomia
				prov = elem.Provincia
				mat = "matricula " +elem.Matricula
				cau = "causada por "+elem.Causa
				pob = elem.Poblacion
				fech = "publicada en "+elem.Fecha
				niv = elem.Nivel
				carr = "Carretera "+elem.Carretera
				p_i = elem.PK_I
				p_f = elem.PK_F
				longitud = " alcance de " + str(abs (float(p_i)-float(p_f)))+ " kilometros"
				sentid = elem.Sentido 
		
				incide =  " " + tipo + " <br>" + auto + "("+prov + ") <br>"+ carr + " <br>"+ cau +  " <br>"+ pob  + " <br>"+ fech + " <br>"+ niv + " <br>"+ mat+ " <br>"+ longitud +"<br><br>"
				Incidencias_canal+= incide



			if todo == "todo":
				respuesta = Incidencias_canal

			elif todo == "prov":
				respuesta = PorProvincia
			elif todo == "tipo":
				respuesta = PorTipo

			else:
				respuesta = PorLongitud
			
			template = get_template("todas.html")
			return HttpResponse(template.render(Context({'Incidencias_canal':respuesta,'act_canal':act_canal,'todo':todo})))   
		
def muestra_revista(request, user): #muestra la revista del usuario
	page = page_user(request,user)
	return HttpResponse(page)

	
def principal(request): #muestra la pagina principal de mi aplicacion
	page = home(request)
	return HttpResponse(page)

def rss_user(request, user_selec): #metodo que muestra el RSS de la pagina del usuario Logeado
	"""/user_selec/rss"""
	if request.method == "GET":
		usuario = Usuarios.objects.get(user_name=user_selec)
		id_user = Usuarios.objects.get(pk=usuario.id)
		incidencias_usuario = id_user.incidencias_user_set.all()        
		noticias = ' '
		for objetos in incidencias_usuario:
			tipo =   '<tipo>'+ objetos.Tipo + '</tipo>'
			auto =  '<autonomia>'+objetos.Autonomia+ '</autonomia>'
			prov =  '<provincia>'+objetos.Provincia+ '</provincia>'
			mat =  '<matricula>' + objetos.Matricula+ '</matricula>'
			cau =  '<causa>'+objetos.Causa+ '</causa>'
			pob = '<poblacion>'+objetos.Poblacion+ '</poblacion>'
			fech =  '<fecha>'+objetos.Fecha+ '</fecha>'
			niv =  '<nivel>'+objetos.Nivel+ '</nivel>'
			carr = '<carretera>'+objetos.Carretera+'</carretera>'
			p_i =  '<PK_I>'+objetos.PK_I+ '</PK_I>'
			p_f =  '<PK_F>'+objetos.PK_F+'</PK_F>'
			
			sentid = objetos.Sentido 
					
			noticias +=  " <item>" + tipo + " <br>" + auto + " <br>"+prov + " <br>"+ carr + " <br>"+ cau +  " <br>"+ pob  + " <br>"+ fech + " <br>"+ niv + " <br>"+ mat+ "<br><br>"
					#respuesta+= incide
			#noticias += '<item><title>'+elem.Tipo +'</title><description>'+elem.Carretera+'</description></item>'   


	template = get_template("feed.rss")
	return render_to_response('feed.rss',{'user_selec':user_selec,'noticias':noticias})



def show_help(request):
	respuesta ='MENU AYUDA'
	template = get_template("help.html")
	return HttpResponse(template.render(Context({'titulo':respuesta})))



def servir_css(request,user):

	ident = Conf_User.objects.get(Ident_User=user)
	color_letra = ident.color_letra
	tamanio_letra= int (ident.tamanio_letra)
	color_fondo = ident.color_menu
	template = get_template("css/css.html")
	return HttpResponse(template.render(Context({'color_letra':color_letra,'tamanio_letra':tamanio_letra,'color_fondo':color_fondo})))



@csrf_exempt
def mylogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
        	login(request, user)
            # Redirect to a success page.
        	return HttpResponseRedirect("/"+username)
        else:
            return HttpResponse("El usuario ya no existe")

    else:
        # Return an 'invalid login' error message.
        return HttpResponse("La cuenta o la clave es incorrecta")


	
def edit_color(request):
	
	if request.user.is_authenticated():
		user = request.user.username
		if request.method == 'GET':
			datos = request.GET['color']
			print "color "+ datos ;
			try:
				objeto = Conf_User.objects.get(Ident_User=user)
				objeto.color_letra = datos # se cambia el color de letra
				objeto.save()  
			except Conf_User.DoesNotExist:
				record = Conf_User(Ident_User= user,color_letra=datos)
				record.save()
	
			return HttpResponseRedirect('/'+user)   
		else:
			return HttpResponse("PERMISO DENEGADO");


def edit_menu(request):
	
	if request.user.is_authenticated():
		user = request.user.username
		if request.method == 'GET':
			datos = request.GET['menu']
			#print "color "+ datos ;
			try:
				objeto = Conf_User.objects.get(Ident_User=user)
				objeto.color_menu = datos # se cambia el color de letra
				objeto.save()  
			except Conf_User.DoesNotExist:
				record = Conf_User(Ident_User= user,color_menu=datos)
				record.save()
	
			return HttpResponseRedirect('/'+user)   
		else:
			return HttpResponse("PERMISO DENEGADO");

@csrf_exempt
def edit_titulo(request):
	
	if request.user.is_authenticated():
		user = request.user.username
		if request.method == 'POST':
			datos = request.POST['titulo']
			#print "color "+ datos ;
			try:
				objeto = Conf_User.objects.get(Ident_User=user)
				objeto.Titulo_revista = datos # se cambia el color de letra
				objeto.save()  
			except Conf_User.DoesNotExist:
				record = Conf_User(Ident_User= user,Titulo_revista=datos)
				record.save()
	
			return HttpResponseRedirect('/'+user)   
		else:
			return HttpResponse("PERMISO DENEGADO");


def edit_tamanio(request):
	
	if request.user.is_authenticated():
		user = request.user.username
		if request.method == 'GET':
			datos = request.GET['tamanio']
			print "tamanio "+ datos ;
			try:
				objeto = Conf_User.objects.get(Ident_User=user)
				objeto.tamanio_letra = datos # se cambia el color de letra
				objeto.save()  
			except Conf_User.DoesNotExist:
				record = Conf_User(Ident_User= user,tamanio_letra=datos)
				record.save()
	
			return HttpResponseRedirect('/'+user)   
		else:
			return HttpResponse("PERMISO DENEGADO");





def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def redirect(request):
    return HttpResponseRedirect("/")


def not_found(request, resource):
   
	return HttpResponseNotFound("<html><body><h2>resource not found</h2></body></html>")
