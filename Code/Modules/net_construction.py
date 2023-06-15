# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 12:18:58 2023
@author: arnaud.maupas
"""
import pandas as pd
import numpy as np


def dsi_table(adj_list, indiv, affiliative_behaviors, behav_obs, tot_obs):
    """Computes the DSI from the dataframe list and empty the diagonals."""
    dsi = pd.DataFrame(0, index=indiv, columns=indiv)
    for i in range(len(affiliative_behaviors)):
        dsi += (adj_list[i] / (behav_obs / tot_obs)
                [affiliative_behaviors[i]]) / len(affiliative_behaviors)
    # The diagonal is emptied.
    np.fill_diagonal(dsi.values, 0)
    return dsi


def dsi_table2(adj_list, indiv, affiliative_behaviors, behav_obs, tot_obs):
    dsi = pd.DataFrame(0, index=indiv, columns=indiv)
    for i in range(len(affiliative_behaviors)):
        mean_dyad_comp = adj_list[i].stack().mean()
        dsi += (adj_list[i] / mean_dyad_comp)
        dsi = dsi / len(affiliative_behaviors)
    # The diagonal is emptied.
    np.fill_diagonal(dsi.values, 0)
    return dsi
    # multi-layer

    # ratio agonistique/affiliatif.
