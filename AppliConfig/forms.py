from django import forms

from .mesClasses import *

global memoryParam
memoryParam = MemParam()

DRINKS = ((None,'Please select a drink type'),(1,'Mocha'),(2,'Espresso'),(3,'Latte'))
#SIZES = ((None,'Please select a drink size'),('s','Small'),('m','Medium'),('l','Large'))

class formulaire(forms.Form):

	ficHand = forms.CharField(label='Chemin fichier de paramètre ', max_length=500, required=False, initial='c:\\temp\\y.yaml')
	message = forms.CharField(label='Message ', max_length=100, required=False,initial='Message')
	section_S = forms.ChoiceField( choices=memoryParam.getListe(), required=False)   # MemParam().getListe() pour charger la liste cfg depuis la classe Parametre

	#choice_field = forms.ChoiceField(choices=MY_CHOICES)
	#choice_field = forms.CharField(label='MY_CHOICES')
class NameForm(forms.Form):
    name = forms.CharField(max_length=255)
    entity = forms.CharField(max_length=255)

