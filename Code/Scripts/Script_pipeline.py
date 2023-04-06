# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 12:17:46 2023

@author: arnaud.maupas
"""

import pandas as pd
import Modules.focal_cleaning as clean
import Modules.class_definition as class_def
import Modules.focal_parsing as pars
import Modules.net_construction as constr
import Modules.net_stat as stat
import Modules.net_viz as viz



affiliative_interactions = ['Grooming', 'Etreinte', 'Jeu social', 'Contact passif']
proximity_association = ['0. Debut du scan', '1. Contact passif', '2. Espace peripersonnel', '3. peri<...<2m', '4. Prox. 2-5 m']
agonistic_interactions = []
directed_interaction = ['Grooming']
undirected_interaction = ['Etreinte', 'Jeu social', 'Contact passif']
social_behaviors = affiliative_interactions + agonistic_interactions + proximity_association



behaviors = affiliative_interactions

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

#Manual adjustment : renommer Groom.er.ee -> Ind
tonkean_focals.data = tonkean_focals.data.replace('Groom.er.ee','Ind', regex=True)

tonkean_focals.filtering(grooming_see=True, non_visible_see=True,
                  short_focal_preprocessing_see=True, save=None, ignore=())

tonkean_focals.data = clean.social_category(tonkean_focals.data, affiliative_interactions = affiliative_interactions, agonistic_interactions = [], proximity_association = proximity_association)
tonkean_focals.data = clean.interactor_direction(tonkean_focals.data, directed_interaction = directed_interaction, undirected_interaction = undirected_interaction, proximity_association = proximity_association)
tonkean_focals.data = clean.column_reorder(tonkean_focals.data)

"""data viz"""

viz.visualisation(tonkean_focals, 5, 5)

"""parsing"""
pars.ind_obs_time(tonkean_focals.data)
a = pars.dyad_obs_time(tonkean_focals.data, tonkean_focals.indiv)
pars.ind_obs_time(tonkean_focals.data)
pars.tot_obs_time(tonkean_focals.data)
pars.behav_obs_time(tonkean_focals.data, affiliative_interactions)
pars.edge_list(tonkean_focals.data, social_behaviors) #edge_list pour les non-orientés : toujours non-symetrique. Pose question de si bien reciproque ?
pars.adj_table(tonkean_focals.data, directed_interaction, social_behaviors, tonkean_focals.indiv, undir_adj_table = True)
behavior_rate_dict = pars.table_dict(tonkean_focals.data, affiliative_interactions,directed_interaction, social_behaviors, tonkean_focals.indiv, undir_adj_table = True) #mettre en dict, dissocier les calculs de taux, l'empty diagonal.

with pd.ExcelWriter('layers.xlsx') as writer:
    for df_name, df in behavior_rate_dict.items():
        df.to_excel(writer, sheet_name=df_name)
        
"""look at proximity"""
#première étape: repets
prox = tonkean_focals.data
prox = prox.loc[prox['Social behavior category'] == 'Proximity association']
scan_count = prox.loc[prox['Behavior'] == '0. Debut du scan']
scan_count = scan_count.groupby('numfocal').sum('Duration (s)')

"""network construction"""
behavior_rate_list = list(behavior_rate_dict.values())
behav_obs = pars.behav_obs_time(tonkean_focals.data, affiliative_behaviors)
tot_obs = pars.tot_obs_time(tonkean_focals.data)
dsi_tonk = constr.dsi_table(behavior_rate_list, tonkean_focals.indiv, affiliative_behaviors, behav_obs, tot_obs)

pars.length_adj(tonkean_focals.data, tonkean_focals.indiv, tonkean_focals.affiliative_behaviors)


"""focal parsing"""



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

rhesus2021 = etho.Focals('../Data/Etho/Raw/Rhesus_2021',
                      open_preprocessed=False, check_empty_col=True, ignore=())

#Manual adjustment : renommer Groom.er.ee -> Ind
rhesus2021.data = rhesus2021.data.replace('Groom.er.ee','Ind', regex=True)

rhesus2021.filtering(grooming_see=True, non_visible_see=True,
                     short_focal_preprocessing_see=True, save=None, ignore=())  # filtering

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

rhesus2022 = etho.Focals('../Data/Etho/Raw/Rhesus_2022_xls',
                      open_preprocessed=False, check_empty_col=True, ignore=())

#Manual adjustment : renommer Groom.er.ee -> Ind
rhesus2022.data = rhesus2022.data.drop(np.where(rhesus2022.data['Behavior']=='4 Position')[0]).reset_index(drop = True)

rhesus2022.filtering(grooming_see=True, non_visible_see=True,
                     short_focal_preprocessing_see=True, save=None, ignore=())  # filtering

for i in grooming.index:
    if (grooming.loc[i, 'Behavior'] == '2 Zone de Grooming') :
        print(re.search("Focal est (.*?)\|", grooming.loc[i, 'Modifiers']).group(1))
    print(i)

grooming = grooming.drop(pd.Series(grooming.loc[grooming['Behavior'] ==
                                                 '2 Zone de Grooming', 'Modifiers'].str.split("|", expand=True)[2]).where(lambda x: x == 'None').dropna().index)

grooming.loc[grooming['Behavior'] == '2 Zone de Grooming', 'Modifiers'].str.split("|", expand=True)[0]
