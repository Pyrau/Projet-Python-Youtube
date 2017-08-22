# -*- coding: utf-8 -*-
"""
Created on Wed May 31 10:21:32 2017

@author: practicas1

C'est le fichier git

"""

from selenium import webdriver #Selenium est la librairie qui contrôle webdriver
import pytube #la librairie de gestion de youtube que j'utilise
import ffmpy #la librairie de gestion de ffmpeg
import os #la librairie de gestion du système (windows il me semble)
import time #la librairie pour le temps, notamment la fonction sleep
import csv #la librairie de gestion des csv
from selenium.webdriver.chrome.options import Options #      librairie de gestion des option, vu que j'ai deja import webdriver c'est en théorie inutil


""" CONFIGURATION """

path_BDD='D:\\Python\\Github\\Playlist Youtube\\base donnée playliste youtube vierge.csv'              # emplacement de la BDD
path_new_BDD='D:\\Python\\Github\\Playlist Youtube\\base donnée playliste youtube vierge.csv'          #emplacement de la création d'une nouvelle BDD
path_adblock=r'C:\Users\pierr\AppData\Local\Google\Chrome\User Data\Default\Extensions\gighmmpiobklfepjocnamgkkbiglidom\3.15.0_0'            # emplacement d'adblock
path_chromedriver=r'D:\Python\Github\Playlist Youtube\chromedriver.exe'                    #emplacement de chrome driver
path_dl=r'D:\Python\Github\Playlist Youtube\Playlist'                # emplacement du dossier de téléchargement des musiques
ndc="ndc"                                                    #nom de  compte youtube
mdp="mdp"                                                #mot de passe youtube


chop = webdriver.ChromeOptions()                                                #création d'une option pour notre webdriver, on appel cette option "chop" (je ne sais pas pourquoi à vrai dire c'est un bout de code que j'ai recopié) 
chop.add_argument(                                                                      #on ajoute une option à nos "options pour webdriver"
    'load-extension={0}'.format(r'C:\Users\pierr\AppData\Local\Google\Chrome\User Data\Default\Extensions\gighmmpiobklfepjocnamgkkbiglidom\3.15.0_0')                                           #pour ajouter un plugin c'est load-extension=lien du fichier. Le mec utilisais le .format pour de la simplicité je suppose, ça marche donc j'ai pas touché
)

rep=input('Avez-vous une base de donnée? O/N').lower()                                      #on demande à l'utilisateur si il a une base de donnée (truc à virer plus tard vu qu'il y aura une configuration via interface)

if rep=='o':                                            # si oui
    #path_BDD=input('insérer le chemin vers votre base de donnée')                                     # à l'origine je demandais l'emplacement de la abse de donnée
#    path_BDD='D:\\Python\\Playlist_youtube\\base donnée playliste youtube.csv'                         # c'est mon chemin vrs la base de donnée, à mettre en config
    f=open(path_BDD,'r+',newline='')                                               # on uovre le fichier en r+ !!!! ca permet lecture et écriture
    reader=csv.reader(f,dialect='excel')                            #le csv sera optimisé pour excel
    liste_musique=list(reader)                                          #on lit le csv qu'on met dans une liste
    indice = 0                                              #il n'y a pas de for normal dans python, on doit s'en sortir avec des tricks comme ca. indice c'est l'indice d'un for normal
    num_items = len(liste_musique)                                          #recuperation de la longueur de la liste des musiques
    while indice < num_items:                                       #tant qu'on est pas arrivé au bout de la liste on continue
        liste_musique[indice] = str(liste_musique[indice])[2:len(liste_musique[indice])-3]                      #on modifie chaque élément de la liste car lors de la lecture en csv, le lecteur ajoute des caractères
        indice = indice + 1                                                 #on incrémente après modification
    
else:
    liste_musique=[]                                                #si il n'y a pas de base de donnée on en crée une
    f=open(path_new_BDD,'w',newline='')                            #pareil faudra modifier le path avec la config, on ouvre en w car on fait que de l'écriture dans ce cas là

        
#url_yt= input("insérer l'url youtube")
#url_yt='https://www.youtube.com'
url_yt='https://accounts.google.com/ServiceLogin?passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fnext%3D%252F%26feature%3Dsign_in_button%26app%3Ddesktop%26hl%3Des%26action_handle_signin%3Dtrue&hl=es&uilel=3&service=youtube'                                              #url de connexion à youtube. Fun fact: c'est un lien espagnol

driver = webdriver.Chrome(path_chromedriver,chrome_options = chop)                                              # le driver c'est notre google chrome automatisé.La 1ere option c'est le path du chromedriver (optionnel, si le chromedriver est dans le meme dossier), la 2eme option c'est nos options google qu'on a paramétré au début
driver.get(url_yt)                                                          # driver.get permet d'ouvrir une url
time.sleep(1)                                           # attente d'une seconde
handles = driver.window_handles                             #il me semble que c'est la gestion des onglets
driver.switch_to_window(handles[0])                         #on switch au handle 0 = 1er onglet = onglet de connexion à youtube = page youtube (quand on lance le programme 2 onglets s'ouvrent: notre url.get et l'onglet d'installation d'adblock, il faut donc revenir sur le 1er)
element = driver.find_element_by_css_selector('.whsOnd.zHQkBf')                 # on va dans l'element "champ identifiant"
element.send_keys(ndc)                                    # on entre nos identifiants dans ce champ
#element = driver.find_element_by_css_selector('.ZFr60d.CeoRYc')
element = driver.find_element_by_css_selector('.RveJvd.snByac')                         #on atteint l'élément "bouton validation"
element.click()                                     # on clique sur le bouton
time.sleep(3)                                       # attente de 3 secondes
#time.sleep(2)
element = driver.find_element_by_css_selector('.whsOnd.zHQkBf')                  # on va dans l'element "champ mot de passe"
element.send_keys(mdp)                                             # on entre notre mot de passe dans ce champ
element = driver.find_element_by_css_selector('.RveJvd.snByac')                      #on atteint l'élément "bouton validation"
element.click()                                                             # on clique sur le bouton
ancient_url='o'                                             # on initialise la variable ancien url
flag=0                                                  # on initialise le drapeau

while 1>0:                                                  # boucle infinie pas très propre...
    try:
        pytube.YouTube(driver.current_url).get_videos()                           # on vérifie si l'utilisateur est sur une page video youtube (si il a un peu surfé pour trouver sa video ca evite de tout faire sauter)       
    except:
        time.sleep(1)                                # on fait la verification chaque seconde
    else:
        if driver.current_url!=ancient_url:                                     # si la page a changé de vidéo
            ancient_url=driver.current_url                          # on récupère le nom de la nouvelle page qui devient la future ancienne
            name=driver.title                                             # on recupere le nom de la page VIA CHROMEDRIVER
            if str('0123456789').find(name[1])!=-1:                       # suppression des (xx) des notifications
                if str('0123456789').find(name[2])!=-1:
                    name=name[5:len(driver.title)-10]
                else:
                    name=name[4:len(driver.title)-10]
            else:                                                 #on enleve les premiers caractère car c'est ecrit Google chrome-
                name=name[0:len(driver.title)-10]
            for musique in liste_musique:                               #on arrive donc au nom tel qu'il est dans la base de donnée : le nom de la vidéo tel qu'il est sur youtube (avec tous les caractères spéciaux)
                if musique==name:                                 #si on retrouve la musique alors on leve le drapeau et on sort
                    flag=1          
            if flag==0:                                                        #si on trouve pas la musique
                liste_musique.append(name)                                    #on l'ajoue àa la liste
                yt_url=driver.current_url                                #on recupère l'url de téléchargement
#                yt_url=yt_url.replace('watch?v','v/')
                yt=pytube.YouTube(yt_url)                                 #on entre l'url dans pytube pour recupérer les infos de la vidéo
#                name=name.replace('|','')                                # on retire toutes les merdes qui font sauter la conversion car nom pytube =/= nom chromedriver
#                name=name.replace('/','')
#                name=name.replace('\\','')
#                name=name.replace('ü','u')
#                name=name.replace('ï','i')
#                name=name.replace('ö','o')
#                name=name.replace('ø','o')
#                name=name.replace('?','')
                name_pytube=yt.filename                                                           # on modifie le nom de la filename téléchargée.... mais visiblement ca marchait pas car il y avait toujours des explosions
                yt.get('3gp','240p').download('D:\\Python\\Playlist_youtube\\Playliste')                            #on dl la qualité qu'on retrouve partout: 240p, 3gp
                path=path_dl + "\\"                                # path à passer dans la config
                extension_in='.3gp'                                               # variable extension d'entrée, c'est la vidéo qu'on a dl donc 3gp
                extension_out='.mp3'                                          # variable extension de sortie, on veut du son donc mp3
                ff = ffmpy.FFmpeg(                                         #paramétrage de ffmpeg
                     inputs={path + name_pytube + extension_in: None},
                     outputs={path + name_pytube + extension_out: None}
                )
                ff.run()                                                             #  lancement de ffmpeg
                os.remove(path + name + extension_in)                                   #on supprime la vidéo téléchargée
                wr=csv.writer(f,dialect='excel')                                       # configuration du rédacteur
                wr.writerow([liste_musique[-1]])                                        #on écrit le dernier élément de la liste: l'élément [-1]. A SAVOIR!! le rédacteur écrit sur la ligne i avec i numéro de l'élément dans la liste. Si je veux juste ajouter un élément en derniere ligne sans l'entrer comme élément i de ma liste, je ne sais pas faire
                f.flush()                                                            # on release tout ce qui est dans le buffer (comme ca si on ouvre le csv pdt que le prgramme erit on voit les modifications)
    time.sleep(5)                                              # on attend 5 sec : toutes les 5 sec le programme vérifie l'url
    flag=0                                                     # on réinitialise le flag
        