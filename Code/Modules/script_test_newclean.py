# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 18:37:28 2023

@author: arnaud.maupas
"""
import pandas as pd
import Modules.focal_cleaning as clean
import Modules.class_definition0_1 as class_def

#definir ça comme un fichier à part.
reference_behavior_table = pd.DataFrame(index=pd.MultiIndex.from_arrays([['ref']*31, list(range(31))], names=('table', 'index')),
                                        columns=['Behavior',
                                                 'Behavioral category'],
                                        data=[['Agress. phys.', '1 Agression'],
                                              ['Deplacement', '1 Agression'],
                                              ['Menace', '1 Agression'],
                                              ['Secoue le support',
                                                  '1 Agression'],
                                              ['0 Presentation', '2 Grooming'],
                                              ['1 Debut Grooming',
                                                  '2 Grooming'],
                                              ['2 Zone de Grooming',
                                                  '2 Grooming'],
                                              ['3 Position', '2 Grooming'],
                                              ['4 Fin Grooming', '2 Grooming'],
                                              ['Etreinte', '3 Affiliation'],
                                              ['Monte', '3 Affiliation'],
                                              ['Portage', '3 Affiliation'],
                                              ['Se repose sur',
                                                  '3 Affiliation'],
                                              ['Sniff', '3 Affiliation'],
                                              ['0. Debut du scan',
                                                  '5 Proximite'],
                                              ['1. Contact passif',
                                                  '5 Proximite'],
                                              ['2. Espace peripersonnel',
                                                  '5 Proximite'],
                                              ['3. peri<...<2m',
                                                  '5 Proximite'],
                                              ['4. Prox. 2-5 m',
                                                  '5 Proximite'],
                                              ['Se gratte', 'Cpt autocentré'],
                                              ['Selfgrooming',
                                                  'Cpt autocentré'],
                                              ['Baillement', 'NaN'],
                                              ['Contact passif', 'NaN'],
                                              ['Erreur', 'NaN'],
                                              ['Forage', 'NaN'],
                                              ['Immobile', 'NaN'],
                                              ['Non-visible', 'NaN'],
                                              ['Se deplace', 'NaN'],
                                              ['Jeu social', 'Jeu'],
                                              ['Lipsmack', 'Mimique faciale'],
                                              ['Mimique faciale', 'Mimique faciale']])
    
data = clean.order_data('../Data/Raw/Tonkean_2021_2', start_end = False)
"""
0:2 1:0 2:4 3:1 4:3
0:5 1:0 2:1 3:2 4:3 5:4 6:6
0:0
"""
data, behav_cor = clean.correct_behavioral_cat(data, reference_behavior_table)

data, empty_col_value = clean.empty_col(data, check = True)


tonkean_focals = class_def.Focals('../Data/Raw/Tonkean_2021_2',
                      open_preprocessed=False, check_empty_col=True, ignore=())

#Manual adjustment : renommer Groom.er.ee -> Ind
tonkean_focals.data = tonkean_focals.data.replace('Groom.er.ee','Ind', regex=True)

tonkean_focals.filtering(grooming_see=True, non_visible_see=True,
                  short_focal_preprocessing_see=True, save=None, ignore=())

data = tonkean_focals.data
tonkean_focals.error_line

rhesus2021 = class_def.Focals('../Data/Raw/Rhesus_2021',
                      open_preprocessed=False, check_empty_col=True, ignore=())

#Manual adjustment : renommer Groom.er.ee -> Ind
rhesus2021.data = rhesus2021.data.replace('Groom.er.ee','Ind', regex=True)

rhesus2021.filtering(grooming_see=True, non_visible_see=True,
                     short_focal_preprocessing_see=True, save=None, ignore=())  # filtering




















