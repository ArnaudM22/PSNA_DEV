# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 10:59:48 2023

@author: arnau
"""
import Modules.net as net
import Modules.neuro as neuro
import Modules.etho as etho

import numpy as np
import re



"""
For rhesus 2806
0:2 1:4 2:1 3:5 4:5 5:3 
0:4 1:5 2:6 3:7 4:8 5:20 6:19 7:25 8:12 9:19 10:14 11:15 12:21 13:22 14:24 15:17 16:20 17:23 18:3
0:14 1:10 2:11 3:12 4:13 5:3
y
None
y
1
700
"""
rhesus2806 = etho.Focals('../Data/Etho/Raw/Strass2806_xls',
                         open_preprocessed=False, check_empty_col=True, ignore=())

rhesus2806.filtering(grooming_see=True, non_visible_see=True,
                     short_focal_preprocessing_see=True, save=None, ignore=())  # filtering

#Manual adjustment : renommer Ulisse en Ulysse
rhesus2806.data = rhesus2806.data.replace('Ulisse','Ulysse', regex=True)
rhesus2806.indiv = tuple(dict.fromkeys(rhesus2806.data.loc[:, 'Subject']))

rhesus2806.visualisation(4, 5, see_table=True)


"""
rhesus1
y
400
y
3
20
"""

rhesus1 = etho.Focals('../Data/Etho/Raw/Rhesus',
                     open_preprocessed=False, check_empty_col=True, ignore=())

#Manual adjustment : renommer Groom.er.ee -> Ind
rhesus1.data = rhesus1.data.replace('Groom.er.ee','Ind', regex=True)

rhesus1.filtering(grooming_see=True, non_visible_see=True,
                 short_focal_preprocessing_see=True, save=None, ignore=())  # filtering
# Rhesus
rhesus1.visualisation(4, 5, see_table=True)

"""Analyses"""
_, _, rhes1_dsi, _ = rhesus1.affiliative_networks_adj()
_, _, rhes2806_dsi, _ = rhesus2806.affiliative_networks_adj()

# rhesus affiliative behaviors 
_, _, rhes1_pre_net_dsi, _ = rhesus1.prenet_NM(
    seed=99)
_, _, rhes2806_pre_net_dsi, _ = rhesus1.prenet_NM(
    seed=99)

# An example of individual (eigenvector centrality and brokerage) and dyadic (distance) properties calculation on rhesus dsi.
centr_brok_rhes1, dist_rhes1 = net.indiv_properties(rhes1_dsi)
centr_brok_rhes2806, dist_rhes2806 = net.indiv_properties(rhes2806_dsi)

# The postnet NM graph are charged.
rhes1_post_net_dsi = net.postnet_NM(rhes1_dsi, seed=99)
rhes2806_post_net_dsi = net.postnet_NM(rhes2806_dsi, seed=99)

#global properties
# Rhesus 
properties_dict_rhes1_pre_net, rhes1_pre_net_p_value = net.glob_properties(
    rhes1_dsi, rhes1_pre_net_dsi)
properties_dict_rhes1_post_net, rhes1_post_net_p_value = net.glob_properties(
    rhes1_dsi, rhes1_post_net_dsi)
properties_dict_rhes2806_pre_net, rhes2806_pre_net_p_value = net.glob_properties(
    rhes2806_dsi, rhes2806_pre_net_dsi)
properties_dict_rhes2806_post_net, rhes2806_post_net_p_value = net.glob_properties(
    rhes2806_dsi, rhes2806_post_net_dsi)

# DSI and neuro comparison 
properties_dict_dsi, p_val_dsi = net.comp(
    [rhes1_dsi, rhes2806_dsi], [rhes1_pre_net_dsi, rhes2806_pre_net_dsi])
properties_dict_dsi, p_val_dsi = net.comp(
    [rhes1_dsi, rhes2806_dsi], [rhes1_post_net_dsi, rhes2806_post_net_dsi])

#partie networkcards
import networkx as nx
import network_cards as nc

rhes1_net = nx.Graph(rhes1_dsi)
nc.NetworkCard(rhes1_net)
