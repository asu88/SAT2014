from django.db import models

# Create your models here.
class Usuarios(models.Model): #Tabla que guarda los usuarios Dados de alta en el sistema Admin
    user_name = models.CharField(max_length = 10) # guarda los nombres de los usuarios dados de alta

class Channel(models.Model): # Tabla que guarda la referencia del canal de la DGT
       Title_Channel = models.CharField(max_length=50) 



class AllIncidencias(models.Model):
	site = models.CharField(max_length=20)
	Tipo = models.TextField()
	Autonomia = models.TextField()
	Provincia = models.TextField()
	Matricula = models.TextField()
	Causa = models.TextField()
	Poblacion = models.TextField()
	Fecha = models.TextField()
	Nivel = models.TextField()
	Carretera = models.TextField()
	PK_I = models.TextField()
	PK_F = models.TextField()
	Sentido = models.TextField()

class  Incidencias(models.Model): # Tabla que almacena los de talles de cada incidencia
    
	Canal =  models.ForeignKey(Channel)
	Tipo = models.CharField(max_length=100)
	Autonomia = models.CharField(max_length=100)
	Provincia = models.CharField(max_length=100)
	Matricula = models.CharField(max_length=100)
	Causa = models.CharField(max_length=100)
	Poblacion = models.CharField(max_length=100)
	Fecha = models.CharField(max_length=100) # Fecha de publicacion en el sitio original
	#Date_Create = models.CharField(max_length = 100) # Fecha en que
	Nivel = models.CharField(max_length=100)
	Carretera = models.CharField(max_length=100)
	PK_I = models.CharField(max_length=100)
	PK_F = models.CharField(max_length=100)
	Sentido = models.CharField(max_length=100)


class Conf_User(models.Model): # Tabla que guarda la informacion configurable por el usuario
    Ident_User = models.CharField(max_length=100) #clave primaria del usuario
    Titulo_revista = models.CharField(max_length=100) # titulo de la pagina
    color_letra = models.CharField(max_length=50) # color de la letra
    tamanio_letra = models.CharField(max_length=50) #tamanio de la letra
    color_menu = models.CharField(max_length=50) # color del menu
    color_login = models.CharField(max_length=50)# color de la cajita de login
    color_pie = models.CharField(max_length=50) # color del pie de pagina


class Incidencias_User(models.Model): # Tabla que relaciona los usuarios con sus incidencias
	Ident_User= models.ForeignKey(Usuarios) #guarda la clave primaria del usuario
	Tipo= models.CharField(max_length=100)   
	Provincia = models.CharField(max_length=100) 
 	Carretera = models.CharField(max_length=100) 
	Fecha = models.CharField(max_length = 50)  #Fecha en que se creo la noticia en el sitio original
	Date_Create = models.DateTimeField('date published')  # Fecha en que se selecciono la incidencia
	Autonomia = models.CharField(max_length=100)
	Matricula = models.CharField(max_length=100)
	Causa = models.CharField(max_length=100)
	Poblacion = models.CharField(max_length=100)
	Nivel = models.CharField(max_length=100)
	PK_I = models.CharField(max_length=100)  # Kilometro de inicio de la inicidencia
	PK_F = models.CharField(max_length=100)  # Kilometro del final de la incidencia
	Sentido = models.CharField(max_length=100)

