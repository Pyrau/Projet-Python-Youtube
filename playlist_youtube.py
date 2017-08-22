# -*- coding: utf-8 -*-
"""
Created on Wed May 31 10:21:32 2017

@author: practicas1

C'est le fichier git

"""

from selenium import webdriver                          # Selenium est la librairie qui contrôle webdriver
import pytube                                           # la librairie de gestion de youtube que j'utilise
import ffmpy                                            # la librairie de gestion de ffmpeg
import os                                               # la librairie de gestion du système (windows il me semble)
import time                                             # la librairie pour le temps, notamment la fonction sleep
import csv                                              # la librairie de gestion des csv
from selenium.webdriver.chrome.options import Options   # librairie de gestion des option


# ##########################################
#
#           CONFIGURATION, SET UP
#
# ##########################################

# Put each files with full path
# TO TRY : Relative path?
path_BDD = ''
path_new_BDD = ''
# path_adblock = r''
path_chromedriver = r''
path_dl = r''
ndc = ""  # nom de  compte youtube
mdp = ""  # mot de passe youtube

# Load chrome extensions
chop = webdriver.ChromeOptions()
chop.add_argument(
    'load-extension={0}'.format(r'C:\Users\pierr\AppData\Local\Google\Chrome\User Data\Default\Extensions\gighmmpiobklfepjocnamgkkbiglidom\3.15.0_0')
)


# ##########################################
#
#               Database reading
#
# ##########################################

# Ask if database exists.
# TODO : CHeck automatically
rep = input('Avez-vous une base de donnée? O/N').lower()

if rep == 'o':
    # r+ = read + write
    f = open(path_BDD, 'r+', newline='')
    reader = csv.reader(f, dialect='excel')
    liste_musique = list(reader)
    indice = 0  # il n'y a pas de for normal dans python, on doit s'en sortir avec des tricks comme ca. indice c'est l'indice d'un for normal
    # recuperation de la longueur de la liste des musiques
    num_items = len(liste_musique)
    while indice < num_items:   # tant qu'on est pas arrivé au bout de la liste on continue
        # on modifie chaque élément de la liste car lors de la lecture en csv, le lecteur ajoute des caractères
        liste_musique[indice] = str(liste_musique[indice])[
            2:len(liste_musique[indice]) - 3]
        indice = indice + 1  # on incrémente après modification

else:
    liste_musique = []
    f = open(path_new_BDD, 'w', newline='')

# ##########################################
#
#               YT CONNECTION
#
# ##########################################

url_yt = 'https://accounts.google.com/ServiceLogin?passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fnext%3D%252F%26feature%3Dsign_in_button%26app%3Ddesktop%26hl%3Des%26action_handle_signin%3Dtrue&hl=es&uilel=3&service=youtube'

driver = webdriver.Chrome(path_chromedriver, chrome_options=chop)
driver.get(url_yt)
time.sleep(1)
handles = driver.window_handles                                     # il me semble que c'est la gestion des onglets
# on switch au handle 0 = 1er onglet = onglet de connexion à youtube = page youtube (quand on lance le programme 2 onglets s'ouvrent: notre url.get et l'onglet d'installation d'adblock, il faut donc revenir sur le 1er)
driver.switch_to_window(handles[0])
element = driver.find_element_by_css_selector('.whsOnd.zHQkBf')     # Field : Account name
element.send_keys(ndc)
element = driver.find_element_by_css_selector(
    '.RveJvd.snByac')                                               # Button : Next
element.click()
time.sleep(3)
element = driver.find_element_by_css_selector('.whsOnd.zHQkBf')     # Field : Password
# on entre notre mot de passe dans ce champ
element.send_keys(mdp)
element = driver.find_element_by_css_selector(
    '.RveJvd.snByac')                                               # Field : Next
element.click()

ancient_url = 'o'
flag = 0

# boucle infinie pas très propre...
while 1 > 0:
    try:
        pytube.YouTube(driver.current_url).get_videos()
    except:
        time.sleep(1)
    else:
        if driver.current_url != ancient_url:                                     # si la page a changé de vidéo
            ancient_url = driver.current_url
            name = driver.title

            # suppression des (xx) des notifications
            if str('0123456789').find(name[1]) != -1:
                if str('0123456789').find(name[2]) != -1:
                    name = name[5:len(driver.title) - 10]
                else:
                    name = name[4:len(driver.title) - 10]
            else:  # on enleve les premiers caractère car c'est ecrit Google chrome-
                name = name[0:len(driver.title) - 10]
            # on arrive donc au nom tel qu'il est dans la base de donnée : le nom de la vidéo tel qu'il est sur youtube (avec tous les caractères spéciaux)
            for musique in liste_musique:
                if musique == name:  # si on retrouve la musique alors on leve le drapeau et on sort
                    flag = 1
            if flag == 0:  # si on trouve pas la musique
                liste_musique.append(name)  # on l'ajoue àa la liste
                yt_url = driver.current_url  # on recupère l'url de téléchargement
#                yt_url=yt_url.replace('watch?v','v/')
                # on entre l'url dans pytube pour recupérer les infos de la vidéo
                yt = pytube.YouTube(yt_url)
#                name=name.replace('|','')                                # on retire toutes les merdes qui font sauter la conversion car nom pytube =/= nom chromedriver
#                name=name.replace('/','')
#                name=name.replace('\\','')
#                name=name.replace('ü','u')
#                name=name.replace('ï','i')
#                name=name.replace('ö','o')
#                name=name.replace('ø','o')
#                name=name.replace('?','')

                # ##########################################
                #
                #          FILE DOWNLOAD AND CONVERT
                #
                # ##########################################
                name_pytube = yt.filename
                yt.get('3gp', '240p').download(
                    'D:\\Python\\Playlist_youtube\\Playliste')
                path = path_dl + "\\"
                extension_in = '.3gp'
                extension_out = '.mp3'
                ff = ffmpy.FFmpeg(  # paramétrage de ffmpeg
                    inputs={path + name_pytube + extension_in: None},
                    outputs={path + name_pytube + extension_out: None}
                )
                ff.run()  # lancement de ffmpeg
                os.remove(path + name + extension_in)
                wr = csv.writer(f, dialect='excel')

                # on écrit le dernier élément de la liste: l'élément [-1].
                # A SAVOIR!! le rédacteur écrit sur la ligne i avec i numéro de l'élément dans la liste.
                # Si je veux juste ajouter un élément en derniere ligne sans l'entrer comme élément i de ma liste, je ne sais pas faire
                wr.writerow([liste_musique[-1]])
                f.flush()
    time.sleep(5)
    flag = 0
