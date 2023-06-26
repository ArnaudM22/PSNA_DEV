# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 17 12:23:05 2023

@author: arnau
"""

import Modules.focal_cleaning as clean
import Modules.class_definition as class_def
import numpy as np
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

'''Tonkean 2021'''


"""
First step : data cleaning.
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

tonkean_focals = class_def.Focals('../Data/raw_data/Tonkean_2021',
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

"""
save
tonkean_focals.data.to_excel(
    '../Data/Cleaned_data_input_format/tonkean_2021.xls')
"""


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

rhesus2021 = class_def.Focals('../Data/raw_data/Rhesus_2021',
                              open_preprocessed=False, check_empty_col=True, ignore=())

# Manual adjustment : renommer Groom.er.ee -> Ind
rhesus2021.data = rhesus2021.data.replace('Groom.er.ee', 'Ind', regex=True)


rhesus2021.filtering(grooming_see=True, non_visible_see=True,
                     short_focal_preprocessing_see=True, save=None, ignore=())  # filtering

# Partie column reorga
rhesus2021.data = clean.social_category(rhesus2021.data, affiliative_interactions=affiliative_interactions, agonistic_interactions=[
], proximity_association=proximity_association)
rhesus2021.data = clean.interactor_direction(rhesus2021.data, directed_interaction=directed_interaction,
                                             undirected_interaction=undirected_interaction, proximity_association=proximity_association)
rhesus2021.data = clean.column_reorder(rhesus2021.data)

"""
save
rhesus2021.data.to_excel(
    '../Data/Cleaned_data_input_format/rhesus_2021.xls')
"""

"""
For the Rhesus 2022 behavioral category correction:
0:2 1:4 2:1 3:5 5:3
0:4 1:5 2:6 4:8 5:13 6:25 7:12 8:13 9:14 10:15 11:21 12:22 13:24 14:17 16:23 18:3
1:15 2:12 3:13 4:14 7:3
y
None
y
1
None
"""

rhesus2022 = class_def.Focals('../Data/raw_data/Rhesus_2022',
                              open_preprocessed=False, check_empty_col=True, ignore=())

# Manual adjustment : renommer Groom.er.ee -> Ind
rhesus2022.data = rhesus2022.data.drop(np.where(
    rhesus2022.data['Behavior'] == '4 Position')[0]).reset_index(drop=True)

rhesus2022.filtering(grooming_see=True, non_visible_see=True,
                     short_focal_preprocessing_see=True, save=None, ignore=())  # filtering

# Partie column reorga
rhesus2022.data = clean.social_category(rhesus2022.data, affiliative_interactions=affiliative_interactions, agonistic_interactions=[
], proximity_association=proximity_association)
rhesus2022.data = clean.interactor_direction(rhesus2022.data, directed_interaction=directed_interaction,
                                             undirected_interaction=undirected_interaction, proximity_association=proximity_association)
rhesus2022.data = clean.column_reorder(rhesus2022.data)

"""
save
rhesus2022.data.to_excel(
    '../Data/Cleaned_data_input_format/rhesus_2022.xls')
"""
