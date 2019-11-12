import glob
import os

class MemParam(object):
	def __init__(self):
		self.nomFichier			= None
		self.structureGlob      = None
		#self.liste 				= (('ts','Très Petit'),('s','Small'),('m','Medium'),('l','Large'),('tl','Très Large'))	
		self.liste 				= (('.','..'),('.','..'))

	def getNomFichier(self):
		return(self.nomFichier)

	def setNomFichier(self,fic):
		self.nomFichier = fic

	def getStructGlob(self):
		return(self.structureGlob)

	def getStructGlobFrom(self,depuis):
		return(self.structureGlob[depuis])

	def setStructGlob(self,struct):
		self.structureGlob = struct.copy()

	def setListe(self,liste):
		self.liste = liste

	def getListe(self):
		return((self.liste))


class MemYamlFilesList(object):
	def __init__(self):
		self.baseRepYamlFiles	= []
		self.debug = None

		print("self.debug :",self.debug)


	def setYamlFileList(self,baseRep,debug): 
		liste = glob.glob(baseRep)
		self.debug = debug

		if len(self.baseRepYamlFiles) != 0:
			del self.baseRepYamlFiles[:]
			
		for fic in liste:
			self.baseRepYamlFiles.append(os.path.basename(fic))

		if self.debug == True:
			for i in liste:
			  print("Fichier yaml depuis classe 'setYamlFileList' :",os.path.basename(i))			

	def getYamlFileList(self):
		return(self.baseRepYamlFiles)

	def getDebugMode(self):
		return(self.debug)




