from django.shortcuts import render
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseRedirect
#from swat import *
from django.http import Http404
from .forms import *
import yaml
from .mesClasses import *
from .mesMethodes import *
from .models import *
from mptt.models import MPTTModel, TreeForeignKey
import sys
import sqlite3
from .initVars import *
import re

# Définition des méthodes utilisées dans application YamlBnpp

debug = True
global line


def searchDictPrev(nb,level,type,structGlob,debug):
    if debug:
        print('From searchDictPrev / nb:',nb,'level:',level,'type:',type)
    for key in range(nb-1,-1,-1):
        if debug:
            print('From searchDictPrev in range loop')
            print('key : ',key)
        
        #structGlob[key][3] est le type
        #structGlob[key][2] est le level
        if structGlob[key][3] == type and structGlob[key][2] == (level -1):
            print("searchDictPrev *OK* :","key:",key,"result:",structGlob[key][0])
            ret = {}
            ret[0] = structGlob[key][0]
            ret[1] = key

            print('Retour from searchDictPrev',ret.items())
            return(ret)

def loadModel(structGlob):

    root = Vitapi.objects.all()         # Collecte de tous les records de la base

    if debug:
        print("**** loadModel DEBUG ****** structGlob ==>",structGlob)

    '''print('--- ROOT loadModel START ---')
    print('root :',len(root))
    print('--- ROOT loadModel END ---')'''

    #Si le modèle n'a pas déjà été chargé
    if len(root)== 0:           
        for k,v in structGlob.items(): 
            if debug:
                print('loadModel <LOAD MODEL> clef:',k,'new:',v[0],'target:',v[1], 'clefTarget:',v[4], "type:",v[3])

            if (k == 0):                        # Racine / premiere ligne
                newNode = Vitapi(name=v[0],clef=0)
                target = None

            else:
                if v[3] == 'DICT':
                    newNode = Vitapi(name=v[0],clef=k)
                    #newNode = Vitapi(name=v[0],clef=k,ligne=k+1,niveau=v[2])

                    if v[1] != 'root' and v[4] != 'None':
                        target = Vitapi.objects.get(name=v[1],clef=v[4])
                    else :
                        target = None



                if v[3] == 'LIST':
                    newNode = Vitapi(name=v[0],clef=k)
                    target = Vitapi.objects.get(name=v[1],clef=v[4])

                    print("================= loadModel =========================")
                    print ('newNode:',newNode)
                    print('target:',target)
                    print('structGlob[key]',structGlob[k])
                    print("==========================================")

                if v[3] == 'PARAM':
                    newNode = Vitapi(name=v[0],clef=k)
                    target = Vitapi.objects.get(name=v[1],clef=v[4])

                    print("================== loadModel ========================")
                    print ('newNode:',newNode)
                    print('target:',target)
                    print('structGlob[key]',structGlob[k])
                    print("==========================================")

            try:
                print("** loadModel TRY **","target:",target,"newNode:",newNode)
                newNode.insert_at(target,position='last-child',save=True)
            except:
                print("** loadModel EXCEPT **","target:",target,"newNode:",newNode)
        return (0) 

    #Si le modèle a déjà été chargé, alors len(root) est supérieur à 0 
    else:
        return (-1)

def importYamlMethod(fichier_,nbLignes):

    # Initialisation Expression Regulière pour traitement fichier source non conforme
    #reg1 = re.compile("(^\s{4,})(\w)")

    reg1 = re.compile("(^\s*\w+\s*)(\:){1,}(.+)")


    # Import Yaml file via lecture de fichier plat

    #fichier = "c:\\temp\\vitapy_example.yaml"
    fichier = BASE_REP + SEPSYST + fichier_

    # Si le fichier est sélectionné via l'ihm, il est différent de 999, renvoyé par la liste de sélection
    if '999' not in fichier:

        if debug:
            print("importYamlMethod : ****************",fichier)
        root = "root"

        #Note JPD : a modifier comme ci-dessous pour prise en compte TAB
        #carSep = tabSep #Provisoire pour mise au point

        init = True                 # Initialisation: premier passage
        structGlob = {}             # clefs : nbLigne/newEntity/position/level
        firstListDetect = False
        firstParamDetect = False

               
        fic = open(fichier,'r')
        if debug:
            print('Nom Fichier',fic.name)

        #Pour suivi fichier trace (compteur de lignes)
        if TraceFicNb == True:
            ficTraceNb = open(BASE_REP + SEPSYST  + TraceFicName, 'w')

        nb=0
        level = 0

        for line in fic:
            line = line.rstrip()

            # Trace par cpt de lignes

            if nb == 0:
                ficTraceNb.write(str(nb+1))
            else :
                ficTraceNb.write('\n' + str(nb+1))

            if debug:
                print("*** DEBUG **** Line ==>",line)

            # Fin de Trace par cpt de lignes

            if len(line) == 0:
                continue

            print("*** 1 ***")

            if EXP_REG_USE :

                print("**** EXPRESSION REGULIERE ACTIVE *****")

                r1 = reg1.search(line)

                if r1:
                
                    if debug:
                        print('span ==> :',r1.span())
                        print('groups ==> :',r1.groups())
                        print('start ==> :',r1.start())
                        print('end ==> :',r1.end())

                    chaine = ""
                    chaine__ = ""
                    nb_=1
                    for i in r1.groups():
                        if nb_ != 3:
                            chaine = chaine + i
                            nb_ +=1
                        else:
                            c=0
                            for j in i.split():
                                print("j:",j)
                                if c == 0:
                                    chaine__ = j
                                    c+=1
                                else:
                                    chaine__ = chaine__ + " " + j         
                    
                    line = chaine + " " + chaine__ 

                    if debug:
                        print("chaine__:",chaine__)
                        print('line :',line)                  
                           
            print("*** 2 ***")

            level = line.count(carSep)
            if carSep == tabSep:
                x = level
            else:
                x = level * nbBlankCarSep

            if init:                #Premier passage (ligne)
                structGlob[nb] = [line[0:-1],root,level,'DICT',None]
                init = False
                if debug:
                    print("======== TRACE DEB ==========")
                    print(" *** INIT ***:",structGlob)
                    print("=========TRACE FIN =========")
                    
            elif init == False and level > 0:

                # **********************
                # Cas des dictionnaires
                # **********************
                if line[-1] == ':' and line[x] != '-': 
                    if debug:
                        print('DICO : structGlob avec nb = ',nb,'level:',level,'===>',structGlob.items())
                    result = searchDictPrev(nb,level,'DICT',structGlob,debug)
                    if result != None:
                        if debug:
                            print("result :", result)
                        structGlob[nb] = [line[x:-1],result[0],level,'DICT',result[1]]
                    
                    firstListDetect = False
                    firstParamDetect = False

                    if debug:
                        print("======== TRACE DEB ==========")
                        print(" *** NON INIT (DICT) ***:",structGlob)
                        print("=========TRACE FIN ==========")
                       
                # ************************************************
                # Cas des listes (avec tiret en premier caractere)
                # ************************************************
                
                if line[-1] != ':' and line[x] == '-':
                    if firstListDetect == False:
                        result = searchDictPrev(nb,level,'DICT',structGlob,debug)    # Search previous DICT only
                        if result != None:
                            if debug:
                                print("result de searchDictPrev() :", result)
                            bufTarget = result[0]
                            bufLevel = level
                            bufKeyTarget = result[1]
                            #structGlob[nb] = [line[x:],result[0],level,'LIST',result[1]]
                            structGlob[nb] = [line[x:],bufTarget,bufLevel,'LIST',bufKeyTarget]
                        firstListDetect = True
                    else:
                        structGlob[nb] = [line[x:],bufTarget,bufLevel,'LIST',bufKeyTarget]
                        firstListDetect = True
                    #else:
                    #    structGlob[nb] = [line[x:],bufTarget,bufLevel,'LISTE',nb]

                    if debug:
                        print("======== TRACE DEB ==========")
                        print(" *** NON INIT (LIST) ***:",structGlob)
                        print("=========TRACE FIN ==========")
                        
                # ***************************************************
                # Autres cas, cad correspondances simples (multiples)
                # ***************************************************
                
                if (line[-1] != ':') and (line[x] != '-') and (line[x:].find(':') != -1):
                    if debug:
                        print("*** DEBUG *** PARAMETRE DETECTE:",line[x:],"firstParamDetect:",firstParamDetect)
                        print("*** DEBUG LIGNE ENTIERE",line)
                    if firstParamDetect == False:
                        if debug:
                            print("*** DEBUG *** Parametre avant searchDictPrev : ","nb:",nb,"level:",level,"structGlob:",structGlob)
                        result = searchDictPrev(nb,level,'DICT',structGlob,debug)
                        if debug:
                            print("*** DEBUG *** Apres searchDictPrev : ","result:",result)
                        firstParamDetect = True
                   
                    else :      #firstParamDetect est à True
                        result = searchDictPrev(nb,level,'DICT',structGlob,debug)
                        if debug:
                            print("structGlob:",structGlob)
                            print("LINE:",line[x:])

                    if result != None:
                        if debug:
                            print("result :", result)
                        bufTarget = result[0]
                        bufLevel = level
                        bufKeyTarget = result[1]
                        structGlob[nb] = [line[x:],bufTarget,bufLevel,'PARAM',bufKeyTarget]
                        
                if debug:
                    print("structGlob en cours:",structGlob)
                    print('*****************')
            
            elif init == False and level == 0:
                structGlob[nb] = [line[0:-1],root,level,'DICT',None]

            nb+=1

            # Note JPD : mettre ici test sur existence de nbLines

            if nb >= int(nbLignes):
                break

        if debug:
            print("======== TRACE DEB ==========")
            print("*** StructGlob Final ***",structGlob)
            print('* Nombre de lignes lues * :',nb)
            print("======== TRACE FIN ==========")

        ret = loadModel(structGlob)     # Chargement de la structure modèle

        if ret == 0:
            ret_ = {}
            ret_[0] = True
            ret_[1] = "OK"
            ret_[2] = nb
            #return(ret_)

        if ret == -1:
            ret_ = {}
            ret_[0] = False
            ret_[1] = "ECHEC: Model Already Loaded ?"
            ret_[2] = 0
            #return(ret_)

    # Si le nom du fichier n'est pas sélectionné via l'ihm
    else :
        ret_ = {}
        ret_[0] = False
        ret_[1] = "ECHEC: Fichier de configuration non sélectionné "
        ret_[2] = 0
        #return(ret_)

    ficTraceNb.close()
    return(ret_)



def exportYamlMethod(fichier_):

    #Si le nom du fichier d'export est renseigné via l'ihm
    if fichier_.strip() != '':

        # Début en Temporaire ci-dessous pour chercher le level Max si utile par la suite
        print('------------------ exportYamlMethod -----------------------')
        conn = sqlite3.connect("C:\\PyProjets\\DataMgt\\dq\\db.sqlite3")
        curBase=conn.cursor()

        # Recherche du nombre de niveau max
        requete = "select max(level) from AppliConfig_vitapi "
        try:
            curBase.execute(requete)
            levelMax = (list(curBase))
            levelMaximum = int(levelMax[0][0])
            print('---- Level Maximum -----: ',levelMaximum)

        except:
            ret_ = {}
            ret_[0] = False
            ret_[1] = "Model inexistant"
            ret_[2] = 0
            return(ret_)

        # Fin Temporaire ci-dessous pour chercher le level Max

        parent = None
        
        root = Vitapi.objects.all()         # Collecte tous les records de la base
        #parent = root.get(level=0)         # Devenu inutile

        '''if debug:
            print("SHOW_vitapi parent : ",parent)
            print("*** Avant FOR ***")'''

        structGlobal = {}

        for xx in root:

            if xx.is_leaf_node():
                if debug:
                    print("---------------------------------",xx,'\n')
                    print("Level",xx.get_level(),'\n')

                    #print("leaf node : ", xx.is_leaf_node())
            
                ancetres = xx.get_ancestors(ascending=False, include_self=True)
                print("ANCESTORS for ",xx," : ",ancetres,'\n')

                anc = ''
                for anc_ in ancetres:
                    anc += str(anc_) + unicodeSep
                anc = anc[:-1]
                print('Ancetres path (clef) :',anc,'\n')

                structGlobal[anc] = xx.get_level(),anc.split(unicodeSep)[:-1]
                print("structGlobal[anc]:",structGlobal[anc])

        if debug:
            print('************************')
            print("*** Apres Boucle FOR ***")
            print('************************')

        print("------ structGlobal ------ : ",structGlobal.items())
        cptTemp = 0
        for k,v in structGlobal.items():
            #print("cpt:",cptTemp)
            #print("------ structGlobal key ------ : ",k)
            #print("------ structGlobal value ------ : ",v)
            cptTemp +=1

        #Construire par la suite la méthode de classe suivante

        listeAffiliation = []
        listeEquation = []
        #structPiloteFic = []

        for clef in structGlobal:

            if debug:
                print('******** Début recherche **********')
            #print('clef :',clef, 'Level :', structGlobal[clef][0], 'Affiliation :',structGlobal[clef][1],'Test :',structGlobal[clef][2])
            if  debug:
                print('clef to search:',clef, 'Niveau :', structGlobal[clef][0], 'Affiliation :',structGlobal[clef][1],'\n')

            if structGlobal[clef][1] not in listeAffiliation:
                print("ABSENT",'\n')
                listeAffiliation.append((structGlobal[clef][1]))

                count = clef.count(unicodeSep)
                listeEquation.append(clef.split(unicodeSep)[count])
                if debug:
                    print('-- listeAffiliation -- :',listeAffiliation,'\n')
                    print('-- listeEquation -- :',listeEquation,'\n')

            else :
                if debug:
                    print('DEJA PRESENT','\n')
                idx_found = listeAffiliation.index(structGlobal[clef][1])
                print('INDEX PRESENCE: ',idx_found,'\n')
                '''
                if debug:
                    print('structGlobal[clef]:',structGlobal[clef])
                    #print('structGlobal:',structGlobal)
                    print('structGlobal[clef][1]:',structGlobal[clef][1])
                    print('listeEquation',listeEquation)
                '''

                try:
                    if debug:
                        print("Début du Try")
                    count = clef.count(unicodeSep)
                    listeEquation[idx_found] = listeEquation[idx_found] + unicodeSep + clef.split(unicodeSep)[count]
                    print('-- structGlobal[clef] --:',structGlobal[clef])
                    print('-- listeAffiliation --:',listeAffiliation,'\n')
                    print('-- listeEquation --:',listeEquation)
                    if debug:
                        print("Fin du Try")

                except:
                    print("*** General Exception Error ***")
                    #print('listeAffiliation[0] :',listeAffiliation[idx_found])

        # Pour vérifier que les 2 structures aient les mêmes dimensions
        '''count = 0
        for xx in listeAffiliation:
            count +=1
        print ('count1 :', count, 'avec len', len(listeAffiliation))
        count = 0
        for xx in listeEquation:
            count +=1
        print ('count2:', count, 'avec len', len(listeEquation))'''

        count = len(listeAffiliation)

        xx = range(count)       # Donc de 0 à ... count (dimension structures)
        
        if debug:
            print('********* Pour Controle des structures *********','\n')
            print("count:",count)
            for i in xx:
                print('range:',i,'\n')
                print('listeAffiliation :',listeAffiliation[i],'\n')
                print('listeEquation :',listeEquation[i],'\n')

          # structPiloteFic pour piloter l'alimentation du fichier de sortie
        if debug:
            print('********* Pour Piloter Structure Alimentation Fichier de sortie *********','\n')
        levelEnCours = 0
        structPiloteFic = []
        INIT = True
        buf = []

        for i in xx:                        # i est la ligne entière de listeAffiliation
            if debug:
                print('Itteration de i :',i)
                print('Affiliation a traiter :',listeAffiliation[i])
            nbLevel = len(listeAffiliation[i])
            nbLoop = 0

            if INIT: 
                print("INIT == True")
                structPiloteFic.append(listeAffiliation[i])
                #print('structPiloteFic : ',structPiloteFic)
                INIT = False
                print("structPiloteFic :",structPiloteFic)

            else :
                buf = []
                print("INIT == False")
                print('nbLevel :',nbLevel)
                yy = range(nbLevel)

                for j in yy:                    # j est l'élément (le Level) de listeAffiliation
                    #print('listeAffiliation [', i, '][',j,'] :',listeAffiliation[i][j])
                    #print('structPiloteFic [', i-1, '][',j,'] :',structPiloteFic[i-1][j])

                    try:
                        if listeAffiliation[i][j] == listeAffiliation[i-1][j]:
                            buf.append('\t')
                            if debug:
                                print('buf_1 :',buf)
                                print('nbLevel_1',nbLevel)
                                print('nbLoop',nbLoop)
                                #print("structPiloteFic :",structPiloteFic)
                            #structPiloteFic[i-1][j] = "99"
                            nbLoop += 1
                            if nbLoop == nbLevel:
                                structPiloteFic.append(buf)
                                if debug:
                                    print("structPiloteFic dans nbLoop :",structPiloteFic)
                                break
                        else:
                            jCur = j
                            while jCur < nbLevel :
                                buf.append(listeAffiliation[i][jCur])
                                jCur+=1
                                if debug:
                                    print('buf_2 :',buf)
                                    #print("structPiloteFic :",structPiloteFic)
                            #buf.append(listeEquation[i])       # EN TEST
                            structPiloteFic.append(buf)
                            if debug:
                                print("structPiloteFic :",structPiloteFic)
                            break

                    except IndexError:
                        print("*** Process Extension Buffer Process ***")
                        jCur = j
                        while jCur < nbLevel :
                            buf.append(listeAffiliation[i][jCur])
                            jCur+=1
                            if debug:
                                print('buf_3 :',buf)
                        #buf.append(listeEquation[i])       # EN TEST
                        structPiloteFic.append(buf)
                        if debug:
                            print("structPiloteFic :",structPiloteFic)
                        break
                    print("---")
            print("------- structPiloteFic -----------",structPiloteFic)
            
        ficChaine = BASE_REP + "\\" + fichier_ + "." + DEF_EXT_FIC
        ficYaml = open(ficChaine,'w')

        cptPlus = 0
        listeEquationBuf = ''

        for i in structPiloteFic:
            listeEquationBuf = ''
            nbElement = len(i)
            if debug:
                print("structPiloteFic en cours [i]",i)
                print('nb Elements :', nbElement)

            cpt = 0
            while cpt < nbElement:
                #nbLines+=1
                #buf = ''

                if cpt == 0 and i[cpt] == '\t':
                    print("* Cas 0 => ", cpt)
                if cpt==0 and i[cpt] != '\t':
                    print("* Cas 1 * => ",i[cpt])
                    #ficYaml.write('*' + str(cpt) + '*' )
                    ficYaml.write(i[cpt] + ':' + '\n')

                if cpt > 0 and i[cpt] != '\t':
                    print("* Cas 2 * => ",i[cpt])
                    print("cpt :",cpt)
                    #ficYaml.write('**' + str(cpt) + '**' )
                    #ficYaml.write('\t'*cpt + i[cpt] + ':' + '\n')
                    ficYaml.write(carSep*cpt + i[cpt] + ':' + '\n')

            
                if cpt == nbElement -1: 
                    print("* Cas 3 * => ",i[cpt]) 
                    print("listeEquation[cptPlus]",listeEquation[cptPlus])                           # Traitement listeEquation
                    #ficYaml.write('\t'*(cpt+1) + 'MAINTENANT' + '\n')
                    for c in listeEquation[cptPlus]:
                        if c == unicodeSep :
                            #c = '\n' + '\t'*(cpt+1)
                            c = '\n' + carSep*(cpt+1)
                        listeEquationBuf = listeEquationBuf + c 
                        #print('c :',c)
                    #ficYaml.write('\t'*(cpt+1) + listeEquationBuf + '\n')
                    print('** listeEquationBuf ** :',listeEquationBuf)
                    ficYaml.write(carSep*(cpt+1) + listeEquationBuf + '\n')
                cpt+=1
            cptPlus+=1
        ficYaml.close()

        ficYaml = open(ficChaine,'r')
        nbLines = 0
        for line in ficYaml:
            nbLines+=1

        ret_ = {}
        ret_[0] = True
        ret_[1] = "OK"
        ret_[2] = nbLines

    #Si le nom du fichier d'export n'est pas renseigné
    else:
        ret_ = {}
        ret_[0] = False
        ret_[1] = "ECHEC : Nom du fichier d'export non renseigné"
        ret_[2] = 0

    return(ret_)
    
    #Fin view exportYaml

               