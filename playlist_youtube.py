#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ##########################################
#
# Author : Pyrau
# Github repository : https://github.com/Pyrau/Projet-Python-Youtube
# License : ???
#
# ##########################################


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
from config import *                                    # Config import

# ##########################################
#
#               Database reading
#
# ##########################################

if os.path.isfile(path_BDD):
    # r+ = read + write
    f = open(path_BDD, 'r+', newline='')
    reader = csv.reader(f, dialect='excel')
    liste_musique = list(reader)
    # num_items = len(liste_musique)
    # for indice in range(0, num_items):
    #     liste_musique[indice] = str(liste_musique[indice])[
    #         2:len(liste_musique[indice]) - 3]

else:
    liste_musique = []
    f = open(path_new_BDD, 'w', newline='')

# ##########################################
#
#               YT CONNECTION
#
# ##########################################

url_yt = 'https://accounts.google.com/ServiceLogin?passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fnext%3D%252F%26feature%3Dsign_in_button%26app%3Ddesktop%26hl%3Des%26action_handle_signin%3Dtrue&hl=es&uilel=3&service=youtube'

# driver = webdriver.Chrome(path_chromedriver, chrome_options=chop)
driver = webdriver.Chrome(path_chromedriver)
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
            yt_url = driver.current_url
            yt = pytube.YouTube(yt_url)

            name = yt.filename
            print(name)
            liste_musique.append([name])  # on l'ajoue à la liste
            
            # ##########################################
            #
            #          FILE DOWNLOAD AND CONVERT
            #
            # ##########################################

            print("Téléchargement vidéo en cours")
            yt.get('3gp', '240p').download(path_dl)
            print("Téléchargement vidéo terminé")
            extension_in = '.3gp'
            extension_out = '.mp3'
            ff = ffmpy.FFmpeg(  # paramétrage de ffmpeg
                inputs={path_dl + name + extension_in: None},
                outputs={path_dl + name + extension_out: None}
            )
            print("Convertissement en musique en cours")
            ff.run()  # lancement de ffmpeg
            print("Convertissement Terminé")
            os.remove(path + name + extension_in)
            wr = csv.writer(f, dialect='excel')

            # on écrit le dernier élément de la liste: l'élément [-1].
            # A SAVOIR!! le rédacteur écrit sur la ligne i avec i numéro de l'élément dans la liste.
            # Si je veux juste ajouter un élément en derniere ligne sans l'entrer comme élément i de ma liste, je ne sais pas faire
            wr.writerow(liste_musique[-1])
            print("Musique ajouté dans la BDD")
            f.flush()
    time.sleep(5)
    flag = 0
