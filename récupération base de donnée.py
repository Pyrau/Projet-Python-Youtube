# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 14:47:39 2017

@author: pierr
"""

import os
import csv


path_base='D:\\Python\\Playlist_youtube\\base donnée playliste youtube.csv'
f=open(path_base,'r+',newline='')
reader=csv.reader(f,dialect='excel')
liste_musique=list(reader)
indice = 0
num_items = len(liste_musique)
while indice < num_items:
    liste_musique[indice] = str(liste_musique[indice])[2:len(liste_musique[indice])-3]
    indice = indice + 1
    
liste=os.listdir(r'D:\Python\Playlist_youtube\Playliste')
indice = 0
num_items = len(liste)
while indice < num_items:
    liste[indice] = str(liste[indice])[0:len(liste[indice])-4]
    liste_musique.append(liste[indice])
    wr=csv.writer(f,dialect='excel')
    wr.writerow([liste_musique[-1]])
    f.flush()
    indice = indice + 1

