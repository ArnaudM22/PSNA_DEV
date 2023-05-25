# -*- coding: utf-8 -*-
"""
Created on Wed May 17 16:38:58 2023

@author: arnau
"""
import networkx as nx
import Modules.datastream_viz as viz
import pandas as pd
import Modules.focal_parsing as pars
import Modules.net_construction as constr
import Modules.net_stat as stat

data = pd.read_excel('../Data/Cleaned_data_input_format/tonkean_2021.xls')
data = data.drop(columns=['Unnamed: 0'])
indiv = pars.indiv_list(data)

affiliative_interactions, proximity_association,  agonistic_interactions, directed_interaction = pars.behaviors_list_def(
    data)


social_behaviors = affiliative_interactions + \
    agonistic_interactions + proximity_association


# first : visualisation
"""data viz"""
# a reprendre
viz.visualisation(data, 5, 5)


"""parsing"""
pars.ind_obs_time(data)
pars.dyad_obs_time(data, indiv)
pars.tot_obs_time(data)
pars.behav_obs_time(data, affiliative_interactions)
# edge_list pour les non-orientés : toujours non-symetrique. Pose question de si bien reciproque ?
pars.edge_list(data, social_behaviors)
pars.adj_table(data, directed_interaction,
               social_behaviors, indiv, undir_adj_table=True)
# mettre en dict, dissocier les calculs de taux, l'empty diagonal.
behavior_rate_dict = pars.table_dict(data, affiliative_interactions,
                                     directed_interaction, social_behaviors, indiv, undir_adj_table=False)
affiliative_behavior_rate_dict = pars.table_dict(data, affiliative_interactions,
                                                 directed_interaction, affiliative_interactions, indiv, undir_adj_table=False)
# dsi
behavior_rate_list = list(affiliative_behavior_rate_dict.values())
behav_obs = pars.behav_obs_time(data, affiliative_interactions)
tot_obs = pars.tot_obs_time(data)
dsi = constr.dsi_table(
    behavior_rate_list, indiv, affiliative_interactions, behav_obs, tot_obs)

a = stat.indiv_properties(dsi)
net = nx.Graph(dsi)
nx.draw(net)
nx.eigenvector_centrality(net)
nx.is_weighted(net)

hud = behavior_rate_dict['Huddling']
with pd.ExcelWriter('layers_tonkean_2021.xlsx') as writer:
    for df_name, df in behavior_rate_dict.items():
        df.to_excel(writer, sheet_name=df_name)

dsi.to_excel('dsi_tonkean_2021.xls')
