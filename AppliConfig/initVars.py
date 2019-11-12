import glob
import os
from .mesClasses import MemYamlFilesList

'''
 **********************************************************************************
Configuration des paramètres initiaux permettant la configuration de l'application
***********************************************************************************
'''

driveConfig = "C:"
repConfig 	= "temp"
ficConfig 	= "config.cfg"
sepWin 		= "\\"
sepLin		= "/"
sep 		= sepWin

unicodeSep = u'\u5E73'

global BASE_REP_YAML
global listeFilesYaml

# Exraction des paramètres applicatif depuis le fichier 'config.txt'

configFile = driveConfig + sep + repConfig + sep + ficConfig

print("***** configFile:",configFile)

ficConf = open(configFile,'r')
nb=0
lineDict = {}

print("Fichier de configuration")

for line in ficConf:
	line = line.strip()
	if line[0:1] not in ('#',''): 
		print('line ',nb,':',line)
		lineDict[nb] = line
		nb+=1
       
ficConf.close()

# Exploitation Dico (Exec)
for k in lineDict:
	print("Exploitation fichier de config : ",k, lineDict[k])
	exec(lineDict[k])

print("--------- Contrôle des paramètres ----------------")
print('BASE_REP:',BASE_REP)
print('DEF_EXT_FIC:',DEF_EXT_FIC)
print('debug:',debug)
print('nbBlankCarSep:',nbBlankCarSep)
print('separator:',separator)

# Réglage des séparateurs dans le fichier source (x blancs ou tab)
#Pour prise en compte blanc multiple (ex: 4 blancs consécutifs)
#nbBlankCarSep = 4
if separator == 'esp':
	carSep = ' ' * nbBlankCarSep

#Pour prise en compte tabulation 
tabSep = '\t'

if separator == 'tab':
	carSep = tabSep

# Répertoire des fichiers yaml et extension par défaut (.yaml)
BASE_REP_YAML = BASE_REP + sep + "*." + DEF_EXT_FIC 

listeFilesYaml = MemYamlFilesList()
listeFilesYaml.setYamlFileList(BASE_REP_YAML,debug)

print ("Liste from the classe",listeFilesYaml.getYamlFileList())

print("Mode Debug :",listeFilesYaml.getDebugMode())



''' Ancienne version à supprimer asap
BASE_REP_YAML = BASE_REP + sep + "*." + DEF_EXT_FIC

liste = glob.glob(BASE_REP_YAML)
listeFicYaml = []


for i in liste:
	  print("Fichier yaml :",os.path.basename(i))

for fic in liste:
	listeFicYaml.append(os.path.basename(fic))

'''