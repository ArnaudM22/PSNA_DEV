# -*- coding: utf-8 -*-
"""
Created on Wed May 17 12:23:05 2023

@author: arnau
"""


affiliative_interactions = ['Grooming',
                            'Etreinte', 'Jeu social', 'Contact passif']
proximity_association = ['0. Debut du scan', '1. Contact passif',
                         '2. Espace peripersonnel', '3. peri<...<2m', '4. Prox. 2-5 m']
agonistic_interactions = []
directed_interaction = ['Grooming']
undirected_interaction = ['Etreinte', 'Jeu social', 'Contact passif']
social_behaviors = affiliative_interactions + \
    agonistic_interactions + proximity_association


behaviors = affiliative_interactions

'''Tonkean'''


"""
First step : data cleaning. Example dataset is Tonkean 2021.
Enter : 
0:2 1:0 2:4 3:1 4:3
0:5 1:0 2:1 3:2 4:3 5:4 6:6
0:0
y
None
y
1
None
"""

tonkean_focals = class_def.Focals('../Data/Raw/Tonkean_2021_2',
                                  open_preprocessed=False, check_empty_col=True, ignore=())

# Manual adjustment : renommer Groom.er.ee -> Ind
tonkean_focals.data = tonkean_focals.data.replace(
    'Groom.er.ee', 'Ind', regex=True)

tonkean_focals.filtering(grooming_see=True, non_visible_see=True,
                         short_focal_preprocessing_see=True, save=None, ignore=())

tonkean_focals.data = clean.social_category(tonkean_focals.data, affiliative_interactions=affiliative_interactions, agonistic_interactions=[
], proximity_association=proximity_association)
tonkean_focals.data = clean.interactor_direction(tonkean_focals.data, directed_interaction=directed_interaction,
                                                 undirected_interaction=undirected_interaction, proximity_association=proximity_association)
tonkean_focals.data = clean.column_reorder(tonkean_focals.data)

tonkean_focals.data.to_excel(
    '../Data/Raw/Cleaned_data_input_format/tonkean_2021.xls')


'''Rhesus 2021'''


"""
For the Rhesus 2021 behavioral category correction:
0:2 1:0 2:4 3:1 4:3
0:5 1:0 2:1 3:2 4:3 5:4 6:6
0:0
y
None
y
1
None
"""

rhesus2021 = class_def.Focals('../Data/Raw/Rhesus_2021',
                              open_preprocessed=False, check_empty_col=True, ignore=())

# Manual adjustment : renommer Groom.er.ee -> Ind
rhesus2021.data = rhesus2021.data.replace('Groom.er.ee', 'Ind', regex=True)

rhesus2021.filtering(grooming_see=True, non_visible_see=True,
                     short_focal_preprocessing_see=True, save=None, ignore=())  # filtering
