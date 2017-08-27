#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ##########################################
#
# Author : Pyrau
# Github repository : https://github.com/Pyrau/Projet-Python-Youtube
# License : ???
#
# ##########################################

import os
import time
import csv
import pytube
import ffmpy
from config import *
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options



def run_connect_chrome(url_yt):
    # driver = webdriver.Chrome(path_chromedriver, chrome_options=chop)
    driver = webdriver.Chrome(path_chromedriver)
    driver.get(url_yt)
    time.sleep(1)
    handles = driver.window_handles
    driver.switch_to_window(handles[0])
    element = driver.find_element_by_css_selector(
        '.whsOnd.zHQkBf')     # Field : Account name
    element.send_keys(ndc)
    element = driver.find_element_by_css_selector(
        '.RveJvd.snByac')                                               # Button : Next
    element.click()
    time.sleep(3)
    element = driver.find_element_by_css_selector(
        '.whsOnd.zHQkBf')     # Field : Password
    element.send_keys(mdp)
    element = driver.find_element_by_css_selector(
        '.RveJvd.snByac')                                               # Field : Next
    element.click()
    print("Connected to Google Chrome")
    return driver


def check_new_url(ancient_url, driver):
    print(driver.current_url)
    if driver.current_url != ancient_url:
        ancient_url = driver.current_url
        yt_url = driver.current_url
        yt = pytube.YouTube(yt_url)
        name = yt.filename
    return name, yt


def convert(path_dl, name):
    extension_in = '.3gp'
    extension_out = '.mp3'
    ff = ffmpy.FFmpeg(
        inputs={path_dl + name + extension_in: None},
        outputs={path_dl + name + extension_out: None}
    )
    print("Convertissement en musique en cours")
    ff.run()
    print("Convertissement Terminé")
    os.remove(path_dl + name + extension_in)


def check_if_in_BDD(liste_musique, name):
    flag = 0
    for musique in liste_musique:
        if musique[0] == name:
            print("musique :" + name + "dans la BDD")
            flag = 1
    return flag


def download(flag, liste_musique, name, path_dl, yt):
    if flag == 0:
        print("musique :" + name + "PAS dans la BDD")
        liste_musique.append([name])

        print("Téléchargement vidéo en cours")
        yt.get('3gp', '240p').download(path_dl)
        print("Téléchargement vidéo terminé")
    return liste_musique


def database_setup(path_BDD):
    if os.path.isfile(path_BDD):
        f = open(path_BDD, 'r+', newline='')
        reader = csv.reader(f, dialect='excel')
        liste_musique = list(reader)

    else:
        liste_musique = []
        f = open(path_BDD, 'w', newline='')
    return liste_musique, f


def main():
    (liste_musique, f) = database_setup(path_BDD)
    url_yt = 'https://accounts.google.com/ServiceLogin?passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fnext%3D%252F%26feature%3Dsign_in_button%26app%3Ddesktop%26hl%3Des%26action_handle_signin%3Dtrue&hl=es&uilel=3&service=youtube'
    driver = run_connect_chrome(url_yt)

    ancient_url = 'o'
    while 1 > 0:
        try:
            pytube.YouTube(driver.current_url).get_videos()
        except:
            time.sleep(1)
        else:
            (name, yt) = check_new_url(ancient_url, driver)
            flag = check_if_in_BDD(liste_musique, name)
            if flag is False:
                liste_musique = download(flag, liste_musique, name, path_dl, yt)
                convert(path_dl, name)
                wr = csv.writer(f, dialect='excel')

                # on écrit le dernier élément de la liste: l'élément [-1].
                # A SAVOIR!! le rédacteur écrit sur la ligne i avec i numéro de l'élément dans la liste.
                # Si je veux juste ajouter un élément en derniere ligne sans l'entrer comme élément i de ma liste, je ne sais pas faire
                wr.writerow(liste_musique[-1])
                print("Musique ajouté dans la BDD")
                f.flush()
                time.sleep(5)
    return


main()
