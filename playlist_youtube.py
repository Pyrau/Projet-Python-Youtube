""" ##########################################
#
# Author : Pyrau
# Github repository : https://github.com/Pyrau/Projet-Python-Youtube
# License : ???
#
########################################## """

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import csv
import pytube
import ffmpy
import config
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options


def check_account():
    """This function check if you have inputed your account"""
    flag_account = 0
    url_connect = 'https://www.youtube.com/'
    if config.ndc != '':
        flag_account = 1
        url_connect = 'https://accounts.google.com/ServiceLogin?passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fnext%3D%252F%26feature%3Dsign_in_button%26app%3Ddesktop%26hl%3Des%26action_handle_signin%3Dtrue&hl=es&uilel=3&service=youtube'
    return flag_account, url_connect


def run_chrome(url_yt):
    """
    Connection to run Chrome
    """
    # driver = webdriver.Chrome(path_chromedriver, chrome_options=chop)
    driver = webdriver.Chrome(config.path_chromedriver)
    driver.get(url_yt)
    time.sleep(1)
    print("Connected to Google Chrome")
    return driver


def connect_to_chrome(driver, flag_account):
    """This function connect to your account that you have setup"""
    if flag_account:
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
        print("Connected to your account")


def database_setup(path_db):
    """
    Setup new or existing database
    """
    if os.path.isfile(path_db):
        database_file = open(path_db, 'r+', newline='')
        reader = csv.reader(database_file, dialect='excel')
        liste_musique = list(reader)

    else:
        liste_musique = []
        database_file = open(path_db, 'w', newline='')
    return liste_musique, database_file


def check_new_url(yt_url, driver):
    """
    Function to check the change of any chrome URL and update it
    """
    if driver.current_url != yt_url:
        yt_url = driver.current_url
        youtube_object = pytube.YouTube(yt_url)
        name = youtube_object.filename
    return name, youtube_object


def check_existence(liste_musique, name):
    """
    Check if tthe video is already in the database and raise a flag to download new video or not
    """
    flag = False
    for musique in liste_musique:
        if musique[0] == name:
            print("musique :" + name + "dans la BDD")
            flag = True
    return flag


def download(liste_musique, name, path_dl, youtube_object):
    """
    Download video
    """
    print("musique :" + name + "PAS dans la BDD")
    liste_musique.append([name])

    print("Téléchargement vidéo en cours")
    youtube_object.get('3gp', '240p').download(path_dl)
    print("Téléchargement vidéo terminé")
    return liste_musique

def convert(path_dl, name):
    """
    Convert videos and extract music then delete video file
    """
    extension_in = '.3gp'
    extension_out = '.mp3'
    ffmpy_options = ffmpy.FFmpeg(
        inputs={path_dl + name + extension_in: None},
        outputs={path_dl + name + extension_out: None}
    )
    print("Convertissement en musique en cours")
    ffmpy_options.run()
    print("Convertissement Terminé")
    os.remove(path_dl + name + extension_in)

def write_into_db(database_file, liste_musique):
    writer_file = csv.writer(database_file, dialect='excel')
    writer_file.writerow(liste_musique[-1])
    print("Musique ajouté dans la BDD")
    database_file.flush()
    time.sleep(5)


def main():
    """
    Main function
    """
    (liste_musique, database_file) = database_setup(config.path_db)
    (flag_account, url_connect) = check_account()
    driver = run_chrome(url_connect)
    connect_to_chrome(driver, flag_account)
    yt_url = 'o'
    while True:
        try:
            pytube.YouTube(driver.current_url).get_videos()
        except:
            time.sleep(1)
        else:
            (name, youtube_object) = check_new_url(yt_url, driver)
            flag = check_existence(liste_musique, name)
            if flag is False:
                liste_musique = download(liste_musique, name, config.path_dl, youtube_object)
                convert(config.path_dl, name)
                write_into_db(database_file, liste_musique)
    return

if __name__ == '__main__':
    main()
