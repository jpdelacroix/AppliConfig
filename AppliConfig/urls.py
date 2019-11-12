
from django.conf.urls import url,handler404
from . import views
from django.contrib import admin 
from django.urls import include, path
from . import views, viewsMppt


app_name = 'AppliConfig'

urlpatterns = [
    url('admin/', admin.site.urls,name='admin'),
    url(r'^$', views.accueil, name='accueil'),
    url('accueil', views.accueil, name='accueil'),
    url('exploitStruct',views.exploitStruct,name='exploitStruct'),
    #MPPT
    url('mppt1',viewsMppt.mppt1,name='mppt1'),
    url(r'^genres/$', viewsMppt.show_genres,name='show_genres'),
    url(r'^callGui/$', viewsMppt.callGui, name='callGui'),
    url(r'^callGui_import/$', viewsMppt.callGui_import, name='callGui_import'),
    url(r'^callGui_export/$', viewsMppt.callGui_export, name='callGui_export'),
    url(r'^importMethod/$', viewsMppt.importMethod, name='importMethod'),
    url(r'^exportMethod/$', viewsMppt.exportMethod, name='exportMethod'),
    url(r'^enTravaux/$', viewsMppt.enTravaux, name='enTravaux'),

    
]
