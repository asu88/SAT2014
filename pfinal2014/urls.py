from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
#from django.views.generic.simple import direct_to_template


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'barrapunto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^admin/', include(admin.site.urls)),
	#url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
	url(r'^login$', 'theapp.views.mylogin'),
	url(r'^logout$', 'theapp.views.logout_view'),
	url(r'^(.*)/css$', 'theapp.views.servir_css'), 
	url(r'^accounts/profile/$', 'theapp.views.redirect'),
    url(r'^accounts/profile/(.*)$', 'theapp.views.page_user'),
   
    
    url(r'^edit/color$', 'theapp.views.edit_color'),	
    url(r'^edit/titulo$', 'theapp.views.edit_titulo'),
    url(r'^edit/tamanio$', 'theapp.views.edit_tamanio'),
    url(r'^edit/menu$', 'theapp.views.edit_menu'),
    url(r'^images/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': 'templates/images'}),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': 'templates/css'}),
    url(r'^init(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': 'templates/init'}),
	#url(r'^incidencias', 'theapp.views.show_incidencias'),
	url(r'^incidencias$', 'theapp.views.show_incidencias'),
	url(r'^todas$', 'theapp.views.show_todas'),
	url(r'^$', 'theapp.views.principal'),  # PAGE Principal
	url(r'^incidencias/(.*)$', 'theapp.views.add_incidencia'),	
	url(r'^update', 'theapp.views.actualizar'),
	url(r'^ayuda$', 'theapp.views.show_help'),
	url(r'^(.*)/rss$', 'theapp.views.rss_user'),
	url(r'^(.*)$', 'theapp.views.page_user') #muestra la pagina del usuario especificado
	#url(r'(.*)', 'theapp.views.not_found'),
	#url(r'^admin/', include(admin.site.urls)),
)
