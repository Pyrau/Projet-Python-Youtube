#!/usr/bin/env python

# ##########################################
#
# This file is used to put user config
# preferences. Put full path of files
#
# When modified, rename file to "config.py"
#
# ##########################################


from selenium import webdriver

path_BDD = r''
path_new_BDD = r''
path_adblock = r''
path_chromedriver = r''
path_dl = r''
ndc = r''  # nom de  compte youtube
mdp = r''  # mot de passe youtube

# Load chrome extensions
chop = webdriver.ChromeOptions()
chop.add_argument(
    'load-extension={0}'.format(r'')
)
