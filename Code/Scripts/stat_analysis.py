# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 26 16:02:23 2023

@author: arnau
"""
import Modules.comparative_stat as comp_stat
import scipy.stats as stats
import numpy as np
import networkx as nx
import Modules.focal_parsing as pars
import Modules.net_stat as stat
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
list_data_sets = ['rhesus_2021', 'tonkean_2021', 'rhesus_2022', 'sai_2023']
dataset_name = 'rhesus_2022'
dataset_name_plot = 'rhesus 2022'
#####

if dataset_name == 'sai_2023':
    affiliative_interactions = ['Proximity', 'Huddling', 'Social play']
    reference_behavior = 'Huddling'
if dataset_name == 'rhesus_2022':
    affiliative_interactions = [
        'Grooming', 'Etreinte', 'Jeu social']
    reference_behavior = 'Grooming'
if dataset_name in ['rhesus_2021', 'tonkean_2021']:
    affiliative_interactions = ['Contact passif',
                                'Grooming', 'Etreinte', 'Jeu social']
    reference_behavior = 'Grooming'
affiliative_interactions = affiliative_interactions + ['dsi']
'''layer_name = 'dsi'
index_list = ['group size', 'density', 'diameter', 'clustering ratio',
              'strength skewness', 'vertex strength variance', 'modularity', 'strength assortativity']
summary_data = pd.DataFrame(index=index_list)'''
########################

# ouverture jeu de données:
xls = pd.ExcelFile('../Data/layers/layers_' + dataset_name + '.xlsx')
#sheet_name = xls.sheet_names
sheet_name = affiliative_interactions
data_dict = pd.read_excel(xls, sheet_name, index_col=0)

summary_data = comp_stat.comparative_pipeline(
    data_dict, dataset_name, dataset_name_plot, affiliative_interactions)
"""
save
summary_data.to_excel('summary_' + dataset_name + '.xlsx')
"""
