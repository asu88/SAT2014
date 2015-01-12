from django.contrib import admin

from models import Usuarios, Channel, Incidencias, Conf_User , Incidencias_User 

admin.site.register(Usuarios)
admin.site.register(Channel)
admin.site.register(Incidencias)
admin.site.register(Conf_User)
admin.site.register(Incidencias_User)
