from django.shortcuts import render
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseRedirect
#from swat import *
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .forms import *
import yaml
from .mesClasses import *
from .mesMethodes import *
from .models import *
from .initVars import *
from mptt.models import MPTTModel, TreeForeignKey
import sys
import sqlite3
from .forms import NameForm

debug = True


def mppt1(request):
	rock = Genre.objects.create(name="Rock")
	blues = Genre.objects.create(name="Blues")
	Genre.objects.create(name="Hard Rock", parent=rock)
	Genre.objects.create(name="Pop Rock", parent=rock)

	vtamodels  = Genre.objects.create(name="vtamodels")
	Genre.objects.create(name="ASSU", parent=vtamodels)
	Genre.objects.create(name="FR", parent=vtamodels)

	return (HttpResponse("OK création réalisée"))


def show_genres(request):
      
   	#data = genreTest.objects.all()
    #print("*******",type(genre_))
	return render(request, "genres.html", {'genres': Genre.objects.all(),'nb':555})

	#return render(request, "genres.html", {'genres': data,'nb':nb})

#def test(request):
#    return render(request, "genres.html", {'genres': Genre.objects.all()})


def show_category(request,hierarchy=None):
#def show_category(request,hierarchy=None):
	category_slug = hierarchy.split('/')
	parent = None
	
	root = Category.objects.all()

	print("SHOW_CATEGORY hierarchy:", hierarchy)
	print("SHOW_CATEGORY root : ",root)
	print("SHOW_CATEGORY category_slug : ",category_slug)
	print("SHOW_CATEGORY parent : ",parent)

	print("avant FOR")
	for slug in category_slug[:-1]:
		print("SHOW_CATEGORY parent__ : ",parent)
		parent = root.get(parent=parent, slug = slug)
		print("parent au root.get() : ",parent)

		print("parent : ",parent)

	print("apres FOR")

	try:
		print("Try: parent :",parent)
		print("Try: category_slug[-1] :",category_slug[-1])
		instance = Category.objects.get(parent=parent,slug=category_slug[-1])
	except:
		print("Exception")
		instance = get_object_or_404(Post, slug = category_slug[-1])
		return render(request, "postDetail.html", {'instance':instance})
	else:
		print("Else")
		return render(request, 'categories.html', {'instance':instance})

	print("the End")
	
def callGui(request):

	# Pour établir la liste des tables SAS dans le répertoire par défaut
	# A écrire dans la table du model
	#for fic in liste:
	 #  print("************",os.path.basename(fic)[:-9])
	
	if request.method == "GET":

		if debug:
			print('****** STEP GET ***************')
			print('****** listeFicYaml ***************',listeFicYaml)

		selectedEntity = 'Vitapis'	# En provisoire

		context={'listeFicYaml':listeFicYaml,'selectedEntity':selectedEntity}
		return render(request, "pages/callGui.html", {'context': context })

def callGui_import(request):

	# Pour établir la liste des tables SAS dans le répertoire par défaut
	# A écrire dans la table du model
	#for fic in liste:
	 #  print("************",os.path.basename(fic)[:-9])

	if request.method == "GET":	
		selectedEntity = 'Vitapis'	# En provisoire
		var = BASE_REP	

		# Fetch dynamique de la liste des ficiers yaml
		#listeFilesYaml = MemYamlFilesList()
		listeFilesYaml.setYamlFileList(BASE_REP_YAML,debug)	
		listeFicYaml = listeFilesYaml.getYamlFileList()

		context={'listeFicYaml':listeFicYaml,'selectedEntity':selectedEntity,'var':var}
		return render(request, "pages/callGui_import.html", {'context': context })

def callGui_export(request):

	# Pour établir la liste des tables SAS dans le répertoire par défaut
	# A écrire dans la table du model
	#for fic in liste:
	 #  print("************",os.path.basename(fic)[:-9])
	
	if request.method == "GET":

		listeFilesYaml.setYamlFileList(BASE_REP_YAML,debug)	
		listeFicYaml = listeFilesYaml.getYamlFileList()

		selectedEntity = 'Vitapis'	# En provisoire

		var = BASE_REP		# From initVars

		context={'listeFicYaml':listeFicYaml,'selectedEntity':selectedEntity,'var':var}
		return render(request, "pages/callGui_export.html", {'context': context })	

	else:
		return(HttpResponse("POST"))	
	
# ------------------------------------------------------------------------------------

	'''elif request.method == "POST":

		selectedEntity = 'Vitapis'

		if debug:
			print('****** STEP POST ***************')
			print('****** listeFicYaml ***************',listeFicYaml)
			#print('****** ListeFic ***************',request.POST['ListeFic'])
  
		SelectedFicName = request.POST['ListeFic']

		flagTest = True
		print("===== SelectedFicName ========>",SelectedFicName)

		context={'listeFicYaml':listeFicYaml,'selectedEntity':selectedEntity,'SelectedFicName':SelectedFicName}
		return render(request, "pages/callGui.html", {'context': context })
		#return(HttpResponse("Retour_ : " + SelectedFicName))'''
	
def importMethod(request):

	selectedEntity = 'Vitapis'
	SelectedFicName = request.POST['ListeFic']
	nbLignes = request.POST['limitNbLin']

	ret = {}

	if nbLignes == '':
		print('NBLIGNES :',nbLignes)
		nbLignes = 2000000

	print('NBLIGNES :',nbLignes)
	
	try:
		ret = importYamlMethod(SelectedFicName,nbLignes)

		if str(ret[2]) != '0':	
			msg = ret[1] + ' * ' + str(ret[2]) + ' lines loaded from ' + BASE_REP + '\\' + SelectedFicName + '.' + DEF_EXT_FIC

		else:
			msg = ret[1]

		fromMethod = "IMPORT_FLAG"
		nbLignes = 0

		listeFicYaml = listeFilesYaml.getYamlFileList()

		context={'listeFicYaml':listeFicYaml,'selectedEntity':selectedEntity,'SelectedFicName':SelectedFicName,'fromMethod':fromMethod,'msg':msg}
		return render(request, "pages/callGui_import.html", {'context': context })

	except:
		print("Exception Format fichier Source")
		msg1 = "Anomalie de structure dans le fichier source "
		msg2 = "Analyse de la structure conseillée "

		if TraceFicNb == True:
			nbCheck = 999
			ficTraceNb = open(BASE_REP + SEPSYST  + TraceFicName, 'r')
			nbLin = ficTraceNb.readlines()
			ficTraceNb.close()
			#nbCheck = nbLin[len(nbLin) -1] 
			context={'SelectedFicName':SelectedFicName,'msg1':msg1,'msg2':msg2, 'nbCheck':nbCheck}
		else :
			context={'SelectedFicName':SelectedFicName,'msg1':msg1,'msg2':msg2}
	
		return render(request, "pages/display_error.html",{'context': context })

def exportMethod(request):

	selectedEntity = 'Vitapis'

	if debug:
		print('****** STEP POST ***************')
		#print('****** listeFicYaml ***************',listeFicYaml)
		#print('****** ListeFic ***************',request.POST['ListeFic'])
  
	SelectedFicName = request.POST['ListeFic']
	#limitNbLin = request.POST['limitNbLin']

	ret = exportYamlMethod(SelectedFicName)

	if str(ret[2]) != '0':									# Si message retournée par exportYamlMethod
		msg = ret[1] + ' * ' + str(ret[2]) + ' lines loaded in ' + BASE_REP + '\\' + SelectedFicName + '.' + DEF_EXT_FIC
	else: 														# Si non
		msg = ret[1]

	fromMethod = "EXPORT_FLAG"
	nbLignes = 0
	var = BASE_REP		# From initVars

	listeFicYaml = listeFilesYaml.getYamlFileList()

	context={'listeFicYaml':listeFicYaml,'selectedEntity':selectedEntity,'SelectedFicName':SelectedFicName,'fromMethod':fromMethod,'msg':msg, 'var':var}
	return render(request, "pages/callGui_export.html", {'context': context })	


def my_view(request):

    name_form = NameForm(request.POST or None, initial={'name': 'whatever','entity':'Pollux'})

    if request.method == 'POST':
        if name_form.is_valid():
            # do something
            print("GOOD !")

    return render(request, 'pages/name-form.html', {'name_form': name_form})

def enTravaux(request):
	return(HttpResponse("<br><hr><div align=center><h1>Encore un peu de patience. En travaux ...</h1></div><br><hr>"))




