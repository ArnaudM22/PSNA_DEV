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

def edge_list2(data, behaviors):
    dir_adj = pd.DataFrame(data.loc[data['Behavior'].isin(behaviors)].groupby(['Behavior', 'Subject', 'Interaction direction', 'Other individual'])[
                           'Duration (s)'].sum(numeric_only = True))  # The duration is calculated for each combination of behavior, individual, and modifiers.
    
    
def edge_lists(data, directed_behaviors, undirected_behaviors):
    # Undirected case.
    undir_adj = pd.DataFrame(data.loc[data['Behavior'].isin(undirected_behaviors)].groupby(['Behavior', 'Subject', 'Other individual'])[
                             'Duration (s)'].sum(numeric_only = True))  # The duration is calculated for each combination of behavior, individual, and modifiers.
    undir_adj = undir_adj.merge(pd.Series(undir_adj.index.get_level_values('Other individual'), index=undir_adj.index).str.split(
        ',', expand=True), left_index=True, right_index=True)  # The names in the modifiers section are separated.
    undir_adj = undir_adj.replace('NaN', np.nan)
    undir_adj2 = undir_adj.loc[:, ['Duration (s)', 0]].dropna().rename(
        columns={0: 'Other individual'})  # undir_adj2 is used for the loop.
    # Modifiers correction.
    for i in range(1, len(undir_adj.columns) - 1):
        undir_adj2 = pd.concat((undir_adj2, undir_adj.loc[:, [
                               'Duration (s)', i]].dropna().rename(columns={i: 'Other individual'})))
    undir_adj = undir_adj2.set_index(undir_adj2.index.droplevel(2)).groupby(
        ['Behavior', 'Subject', 'Other individual']).sum(numeric_only = True)  # Summed values for Modifiers.
    # Directed case.
    dir_adj = pd.DataFrame(data.loc[data['Behavior'].isin(directed_behaviors)].groupby(['Behavior', 'Subject', 'Interaction direction', 'Other individual'])[
                           'Duration (s)'].sum(numeric_only = True))  # The duration is calculated for each combination of behavior, individual, and modifiers.
    
    
    # Directed case.
    dir_adj = pd.DataFrame(data.loc[data['Behavior'].isin(directed_behaviors)].groupby(['Behavior', 'Subject', 'Modifiers'])[
                           'Duration (s)'].sum(numeric_only = True))  # The duration is calculated for each combination of behavior, individual, and modifiers.
    dir_adj = dir_adj.merge(pd.Series(dir_adj.index.get_level_values('Modifiers'), index=dir_adj.index).str.split('|', expand=True), left_index=True,
                            right_index=True).rename(columns={0: 'direction', 1: 'Modifiers'}).set_index(dir_adj.index.droplevel(2))  # Modifiers separation.
    # A subject column is created.
    dir_adj.loc[:, 'Subject'] = dir_adj.index.get_level_values(1)
    # Lines with "None" values are deleted.
    dir_adj = dir_adj.replace('None', np.nan).dropna(axis=0)
    dir_adj.loc[dir_adj['direction'] == 'Focal est recepteur', ['Modifiers', 'Subject']] = dir_adj.loc[dir_adj['direction'] ==
                                                                                                       'Focal est recepteur', ['Subject', 'Modifiers']].values  # Subject and Modifiers are reversed to always have the sender as subject.
    # Removal of the Subject index column and replace it with the Subject column
    dir_adj = dir_adj.set_index(dir_adj.index.droplevel(1))
    # The summed values for each individual in Modifiers are calculated.
    dir_adj = dir_adj.groupby(['Behavior', 'Subject', 'Modifiers']).sum(numeric_only = True)
    return undir_adj, dir_adj
    
def adj_table(data, directed_behaviors, undirected_behaviors, behaviors, indiv_list, undir_adj_table = False):
    """"Calculates a multi-index dataframe sumarizing the informations for all the affiliative behaviors (directed and undirected)."""
    undirec, direc = edge_lists(data, directed_behaviors, undirected_behaviors)
    # The index is initialized.
    iterables = [behaviors, indiv_list, indiv_list]
    index = pd.MultiIndex.from_product(
        iterables, names=['Behavior', 'Subject', 'Modifiers'])
    # The dataframe is filled.
    adj = pd.DataFrame(index=index).merge(pd.concat(
        (undirec, direc)), how='left', right_index=True, left_index=True).fillna(0).unstack(1)
    adj.columns = adj.columns.droplevel()
    # The non-oriented behaviors are symmetrized.
    for i in undirected_behaviors:
        adj.loc[i] = (adj.loc[i].transpose() + adj.loc[i]).values
    if undir_adj_table == True : 
        for i in directed_behaviors:
            adj.loc[i] = (
                adj.loc[i].transpose() + adj.loc[i]).values
    return adj


def table_list(data, directed_behaviors, undirected_behaviors, behaviors, indiv_list, undir_adj_table = False):
    """Converts the multi-index dataframe containing the data into a dataframe 
    list and empty the diagonals."""
    
    table = adj_table(data, directed_behaviors, undirected_behaviors, behaviors, indiv_list, undir_adj_table)
    dyad_obs = dyad_obs_time(data, indiv_list)
    adjlist = []
    for i in behaviors:
        # The diagonals is emptied.
        np.fill_diagonal(table.loc[i].values, 0) #see if that is what we want.
        # The table is added to the list.
        adjlist.append(table.loc[i])
    # The rates are calculated.
    adjlist = list(map(lambda x: x.div(dyad_obs), adjlist))
    return adjlist


#proximité