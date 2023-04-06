# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 17:56:18 2023

@author: arnaud.maupas
"""
import numpy as np
import pandas as pd

def ind_obs_time(data):
    ind_time_list = data.groupby('numfocal').first().groupby('Subject').sum(numeric_only = True).loc[:,'focal_length']
    return ind_time_list

def tot_obs_time(data):
    tot_time = ind_obs_time(data).sum()
    return tot_time

def dyad_obs_time(data, indiv_list):
    ind_obs = ind_obs_time(data)
    dyad_obs_time = pd.DataFrame(0, index= indiv_list, columns= indiv_list)
    for i in range(len(dyad_obs_time)):
        dyad_obs_time.iloc[i] = ind_obs + ind_obs.iloc[i]
    return dyad_obs_time
        
def behav_obs_time(data, behavior_list):
    behav_obs = data.loc[data['Behavior'].isin(behavior_list)].groupby(
        'Behavior')['Duration (s)'].sum()
    return behav_obs

def edge_list(data, behaviors):
    # Correction des other individual multiples
    inter_list = pd.DataFrame(data.loc[data['Behavior'].isin(behaviors)].groupby(['Behavior', 'Subject', 'Interaction direction', 'Other individual'])[
                           'Duration (s)'].sum(numeric_only = True))  # The duration is calculated for each combination of behavior, individual, and modifiers.
    inter_list = inter_list.merge(pd.Series(inter_list.index.get_level_values('Other individual'), index=inter_list.index).str.split(
        ',', expand=True), left_index=True, right_index=True)  # The names in the modifiers section are separated.
    inter_list = inter_list.replace('NaN', np.nan)
    inter_list2 = inter_list.loc[:, ['Duration (s)', 0]].dropna().rename(
        columns={0: 'Other individual'})  # undir_adj2 is used for the loop.
    # Modifiers correction.
    for i in range(1, len(inter_list.columns) - 1):
        inter_list2 = pd.concat((inter_list2, inter_list.loc[:, [
                               'Duration (s)', i]].dropna().rename(columns={i: 'Other individual'})))
    inter_list = inter_list2.set_index(inter_list2.index.droplevel(3)).groupby(
        ['Behavior', 'Subject', 'Interaction direction', 'Other individual']).sum(numeric_only = True)  # Summed values for Modifiers.
    # Correction des comportements dirigés
    inter_list.loc[:,['Subject', 'Interaction direction','Other individual']] = inter_list.reset_index().loc[:,['Subject', 'Interaction direction','Other individual']].values
    # Lines with "None" values are deleted.
    inter_list = inter_list.replace('None', np.nan).dropna(axis=0)
    inter_list.loc[inter_list['Interaction direction'] == 'Focal est recepteur', ['Other individual', 'Subject']] = inter_list.loc[inter_list['Interaction direction'] == 'Focal est recepteur', ['Subject', 'Other individual']].values  # Subject and Modifiers are reversed to always have the sender as subject.
    #inter_list.loc[inter_list['Interaction direction'] == 'Focal est recepteur', 'Interaction direction'] = 'Focal est emetteur'
    # Removal of the Subject index column and replace it with the Subject column
    inter_list = inter_list.set_index(inter_list.index.droplevel((1, 2 , 3)))
    # The summed values for each individual in Modifiers are calculated.
    inter_list = inter_list.groupby(['Behavior', 'Subject', 'Other individual']).sum(numeric_only = True)
    return inter_list

        
def adj_table(data, directed_interaction, behaviors, indiv_list, undir_adj_table = False):
    """"Calculates a multi-index dataframe sumarizing the informations for all the affiliative behaviors (directed and undirected)."""
    inter_list  = edge_list(data, behaviors)
    # The index is initialized.
    iterables = [behaviors, indiv_list, indiv_list]
    index = pd.MultiIndex.from_product(
        iterables, names=['Behavior', 'Subject', 'Other individual'])
    # The dataframe is filled.
    adj = pd.DataFrame(index=index).merge(inter_list, how='left', on = ['Behavior', 'Subject', 'Other individual']).fillna(0).unstack(1)
    adj.columns = adj.columns.droplevel()
    # The non-oriented behaviors are symmetrized.
    for i in list(set(behaviors) - set(directed_interaction)):
        adj.loc[i] = (adj.loc[i].transpose() + adj.loc[i]).values
    if undir_adj_table == True : 
        for i in directed_interaction:
            adj.loc[i] = (
                adj.loc[i].transpose() + adj.loc[i]).values
    return adj


def table_dict(data, rate_behavior, directed_interaction, behaviors, indiv_list, undir_adj_table = False):
    """Converts the multi-index dataframe containing the data into a dataframe 
    list and empty the diagonals."""
    table = adj_table(data, directed_interaction, behaviors, indiv_list, undir_adj_table)
    dyad_obs = dyad_obs_time(data, indiv_list)
    adjdict = {key: None for key in behaviors}
    for i in behaviors:
        # The diagonals is emptied.
        np.fill_diagonal(table.loc[i].values, 0) #see if that is what we want.
        if i in rate_behavior:
            # The rates are calculated (it was vectorized in last version)
            table.loc[i] = (table.loc[i] / dyad_obs).values
        # The table is added to the dict.
        adjdict[i] = table.loc[i]
    return adjdict


#proximité