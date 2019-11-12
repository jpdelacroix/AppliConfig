from django.shortcuts import render
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseRedirect
#from swat import *
from django.http import Http404
from .forms import *
import yaml
import swat
from .mesClasses import *

global cfg
cfg={}

global context
context={}

'''global memoryParam
memoryParam = MemParam()'''

def accueil(request):

	dictFlag={}

	cfg={}
	flag = 0

	if request.method == 'POST':
		form = formulaire(request.POST)

		if form.is_valid():
			#print("debug cleaned data:",form.cleaned_data['ficHand'],"***",form.cleaned_data['message'])
			try:
				with open(form.cleaned_data['ficHand'],'r') as ymlfile:
					cfg = yaml.load(ymlfile)

				flag = 1

				print("*** ",request.method, "GET with flag :",flag," *** ")
				for section in cfg:						# Affichage de toutes les sections
					print("section ===> ",section)


			except:
				print("ERREUR OUVERTURE FICHIER DE PARAMETRES " + "'" +  form.cleaned_data['ficHand'] + "'")
				cfg={}
				flag = -1

		else :		# Paramètres formulaire non validés
			print("ERREUR FORM IS NOT VALID")

	else :							#GET
		print("** GET *** ",request.method, " with flag :",flag," ***** ")
		form = formulaire()	# Pas de Bind des données et formulaire (vide)
	
	if flag == 1:

		memoryParam.setNomFichier(request.POST['ficHand'])
		print("DEBUG classe MemParam (ficHand) :",memoryParam.getNomFichier())

		memoryParam.setStructGlob(cfg)
		print("DEBUG classe MemParam (cfg) :",memoryParam.getStructGlob())

			# Recherche le noms des sections de la structure, sous forme de tuples, pour alimenter la (les) liste(s) boxe(s)

		MonTuple = []
		for section in cfg:
			#if section != 'THEBAIDE':
			#	section = section + '__'
			cfgTuple = (section,section)
			#cfgTuple = (section)
			MonTuple.append(cfgTuple)
		print("========= - MonTuple - =========>",MonTuple)

		# fin code ici à mettre ailleurs JPD

		form.fields['section_S'].choices = MonTuple  # Liste des sections dans la listebox affichée
		
		dictFlag['flag1'] = flag
		print("dictFlag['flag1'] :",dictFlag.items())
		
		context = {'form':form, 'dictFlag':dictFlag, 'cfg':cfg}
		return render(request,'pages/exploitStruct.html',{'context':context})

	else:
		versSwat= swat.__version__
		print("========== version swat ========>",swat.__version__)

		dictFlag['flag1'] = flag
		context = {'form':form, 'dictFlag':dictFlag, 'cfg':cfg,'versSwat':versSwat}
		return render(request,'pages/accueil.html',{'context':context})



def display_section(request,secName):

	dictFlag={}
	flag = 1
	dictFlag['flag1'] = flag

	cfgPart = memoryParam.getStructGlobFrom(secName)
	memoryParam.setStructGlob(cfgPart)
	#form.fields['part'].choices = PART_CHOICES

	MonTuple = []
	for section in cfgPart:
		cfgTuple = (section,section)   # Utile si utilisation de Choicefields Django
		#cfgTuple = (section)
		MonTuple.append(cfgTuple)
		
	form = formulaire(request.POST)
	form.fields['section_S'].choices = MonTuple

	print("================= secname =====================", secName)
	print("================= cfgPart =====================", cfgPart)

	#return HttpResponse(cfgPart + "azerty")
	context = {'form':form, 'dictFlag':dictFlag, 'cfg':cfgPart}

	return render(request,'pages/exploitStruct.html',{'context':context})
	#return HttpResponse(cfgPart)

def exploitStruct(request):

	'''form = formulaire(request.POST)

	if form.is_valid():
		return HttpResponse(request.POST["aa"])
	else:
		return HttpResponse("hs")'''

	if request.method == "POST":
		print('POST')
		form = formulaire(request.POST)
		if form.is_valid():
			print('VALID')
			ch = form.cleaned_data['ficHand']
			print('ch','.',ch,'.')
			#print('x',form.cleaned_data['id_aa'],'y')

		else:
			print("BAD")
	return render(request,'pages/exploitStruct.html',{'context':context})
	


''' Note JPD : faire traitement exception ici '''

'''	
chaine = ""	    
for section in cfg:
	chaine = section + chaine + "\n"
    #print("section :",section)

print()
print("cfg['mysql']",cfg['mysql'])
print("cfg['other']",cfg['other'])
print("cfg['test']",cfg['test'])
print()

print("*** :",cfg['vtamodels']['SECURINTELL']['EN'])
print()
print(cfg['Parametrage Listes']['DQ_LANGUAGES'])
print(cfg['actionsets'])
print('os.environ',cfg['os.environ'])
print()
print(cfg.keys())
print('VI_RELEASE : ',cfg['VI_RELEASE'])
print('-----------')
aa = cfg['json_map']
print(type(aa))
print(aa['key'])

print(cfg["concepts"].keys())
print(cfg["concepts"].items())
for i in cfg["concepts"]:
    print(i," * ",cfg["concepts"][i])
   
print(cfg['concepts_persons'])


form = formulaire()

print("*** form ******", type(form))

with open("C:\\Paramètrage Python\\yaml.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

print("POLLUX ",cfg['Parametrage Listes']['DQ_LANGUAGES'])
lang = cfg['Parametrage Listes']['DQ_LANGUAGES']
context = {'dqLang':lang, 'form':form}

return HttpResponse(cfg['Parametrage Listes']['DQ_LANGUAGES'])
#return render(request, "pages/Accueil.html", {'context': context})
#return render(request, "pages/Accueil.html",{'context': context})
'''