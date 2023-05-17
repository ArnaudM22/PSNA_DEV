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

path = '../../saimiris/DataCollectionBORIS/Post_Process_xls'

# import and merge
data = pd.concat(map(pd.read_excel, glob.glob(
    os.path.join(path, '*.xls'))), ignore_index=True)

data = data.sort_values(
    ["Observation id", "Start (s)"], ignore_index=True)
# A numerical identifier is assigned to each focal length (2 lines are in the same focal length if they are consecutive with the same observation_id and the same subject).
data.loc[:, 'numfocal'] = (data.loc[:, ['Observation id', 'Subject']] != data.loc[:, [
                           'Observation id', 'Subject']].shift()).any(axis=1).cumsum() - 1

indiv = tuple(dict.fromkeys(data.loc[:, 'Subject']))
data.loc[data['Subject'] == 'Jaune-Rose Foncé']
data.loc[data['Subject'] == 'Rose foncé-Jaune']
data.loc[data['Subject'] == 'nan']
