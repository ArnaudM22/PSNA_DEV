# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:44:43 2023

@author: arnau
"""

from pyexcel_xls import save_data
from pyexcel_ods3 import get_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import os
import glob
from collections import Counter
import shutil
import pyexcel_xls
import pyexcel_ods3

path = '../../Projet_Saimiri/post-processed_files'

path = '../../saimiris/DataCollectionBORIS/Post-Process'

# Placer dans un nouveau dossier
# recuperer liste des fichiers au format ods
list_name = []
for subdir in os.listdir(path):
    list_name.append(glob.glob(os.path.join(path, subdir, '*.ods')))

list_name = [ele for ele in list_name if ele != []]
list_name = sum(list_name, [])

# get the true file name list
target_path = 'C:/Users/arnau/Desktop/StageImalis/PSNA_DEV/Data/Raw/Sai_xls_2'
target_path_list = []
for file in list_name:
    file_name = os.path.basename(file)
    target_name = target_path + '/' + file_name
    target_path_list.append(target_name)

# supress hidden file
# list_name[8]
# list_name.pop(8)
# target_path_list[8]
# target_path_list.pop(8)
# copy paste files
for i in range(len(list_name)):
    shutil.copyfile(list_name[i], target_path_list[i])

# conversion noms

for file in target_path_list:
    name = os.path.splitext(file)[0]
    data = pyexcel_ods3.get_data(name + '.ods')
    pyexcel_xls.save_data(name + '.xls', data)

# remove ods
dir_name = target_path
test = os.listdir(dir_name)

for item in test:
    if item.endswith(".ods"):
        os.remove(os.path.join(dir_name, item))
