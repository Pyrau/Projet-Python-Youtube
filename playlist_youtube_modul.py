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
import config
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options



def run_connect_chrome(url_yt):
    """
    Connection to run Chrome and automatically connect to your YT account
    """
    # driver = webdriver.Chrome(path_chromedriver, chrome_options=chop)
    driver = webdriver.Chrome(config.path_chromedriver)
    driver.get(url_yt)
    time.sleep(1)
    handles = driver.window_handles
    driver.switch_to_window(handles[0])
    element = driver.find_element_by_css_selector(
        '.whsOnd.zHQkBf')     # Field : Account name
    element.send_keys(config.ndc)
    element = driver.find_element_by_css_selector(
        '.RveJvd.snByac')                                               # Button : Next
    element.click()
    time.sleep(3)
    element = driver.find_element_by_css_selector(
        '.whsOnd.zHQkBf')     # Field : Password
    element.send_keys(config.mdp)
    element = driver.find_element_by_css_selector(
        '.RveJvd.snByac')                                               # Field : Next
    element.click()
    print("Connected to Google Chrome")
    return driver


def check_new_url(yt_url, driver):
    """
    Function to check the change of any chrome URL and update it
    """
    print("in check_new_url")
    if driver.current_url != yt_url:
        print(driver.current_url)
        print(yt_url)
        yt_url = driver.current_url
        yt = pytube.YouTube(yt_url)
        name = yt.filename
    return name, yt


def convert(path_dl, name):
    """
    Convert videos and extract music then delete video file
    """
    print("in convert")
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
    """
    Check if tthe video is already in the database and raise a flag to download new video or not
    """
    print("in check_if_in_BDD")
    flag = 0
    for musique in liste_musique:
        if musique[0] == name:
            print("musique :" + name + "dans la BDD")
            flag = 1
    return flag


def download(flag, liste_musique, name, path_dl, yt):
    """
    Download video
    """
    print("in download")
    if flag == 0:
        print("musique :" + name + "PAS dans la BDD")
        liste_musique.append([name])

        print("Téléchargement vidéo en cours")
        yt.get('3gp', '240p').download(path_dl)
        print("Téléchargement vidéo terminé")
    return liste_musique


def database_setup(path_BDD):
    """
    Setup new or existing database
    """
    if os.path.isfile(path_BDD):
        f = open(path_BDD, 'r+', newline='')
        reader = csv.reader(f, dialect='excel')
        liste_musique = list(reader)

    else:
        liste_musique = []
        f = open(path_BDD, 'w', newline='')
    return liste_musique, f


def main():
    """
    Main function
    """
    (liste_musique, f) = database_setup(config.path_BDD)
    url_yt = 'https://accounts.google.com/ServiceLogin?passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fnext%3D%252F%26feature%3Dsign_in_button%26app%3Ddesktop%26hl%3Des%26action_handle_signin%3Dtrue&hl=es&uilel=3&service=youtube'
    driver = run_connect_chrome(url_yt)

    yt_url = 'o'
    while 1 > 0:
        try:
            pytube.YouTube(driver.current_url).get_videos()
        except:
            time.sleep(1)
        else:
            (name, yt) = check_new_url(yt_url, driver)
            flag = check_if_in_BDD(liste_musique, name)
            if flag == 0:
                liste_musique = download(flag, liste_musique, name, config.path_dl, yt)
                convert(config.path_dl, name)
                wr = csv.writer(f, dialect='excel')

                wr.writerow(liste_musique[-1])
                print("Musique ajouté dans la BDD")
                f.flush()
                time.sleep(5)
    return


main()
