# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 12:18:58 2023

@author: arnaud.maupas
"""
import pandas as pd
import numpy as np

def length_adj(data, indiv, affiliative_behaviors):
    """"Calculates different durations (dyadic, behavioral and total) used for 
    the construction of affiliative/DSI networks"""

    # The individual observation duration is calculated.
    ind_obs = (data.groupby(['numfocal', 'Subject']).last(
    ).loc[:, 'focal_length']).groupby('Subject').sum()
    # The dyadic observation duration is calculated ('self-dyads' are considered non-Null for the moment).
    dyad_obs = pd.DataFrame(0, index=indiv, columns=indiv)
    for i in range(len(dyad_obs)):
        dyad_obs.iloc[i] = ind_obs + ind_obs.iloc[i]
    # The total observation duration is calculated.
    tot_obs = dyad_obs.to_numpy().sum()/2
    # The behavioral observation durations are calculated.
    behav_obs = data.loc[data['Behavior'].isin(affiliative_behaviors)].groupby(
        'Behavior')['Duration (s)'].sum()
    return dyad_obs, tot_obs, behav_obs

def adj_table(undirec, direc, affiliative_behaviors, indiv):
    """"Calculates a multi-index dataframe sumarizing the informations for all the affiliative behaviors (directed and undirected)."""

    # The index is initialized.
    iterables = [affiliative_behaviors, indiv, indiv]
    index = pd.MultiIndex.from_product(
        iterables, names=['Behavior', 'Subject', 'Modifiers'])
    # The dataframe is filled.
    adj = pd.DataFrame(index=index).merge(pd.concat(
        (undirec, direc)), how='left', right_index=True, left_index=True).fillna(0).unstack(1)
    adj.columns = adj.columns.droplevel()
    # The non-oriented behaviors are symmetrized.
    for i in ['Etreinte', 'Jeu social', 'Contact passif']:
        adj.loc[i] = (adj.loc[i].transpose() + adj.loc[i]).values
    return adj

def undir_adj_table(adj):
    """Produces an undirected version of the adjacency matrices by summing 
    the matrices of the directed behaviors with their transposes."""

    undir_adj = adj.copy(deep=True)
    for i in ['Grooming']:
        undir_adj.loc[i] = (
            undir_adj.loc[i].transpose() + undir_adj.loc[i]).values
    return undir_adj

def table_list(table, affiliative_behaviors, dyad_obs):
    """Converts the multi-index dataframe containing the data into a dataframe 
    list and empty the diagonals."""

    adjlist = []
    for i in affiliative_behaviors:
        # The diagonals is emptied.
        np.fill_diagonal(table.loc[i].values, 0)
        # The table is added to the list.
        adjlist.append(table.loc[i])
    # The rates are calculated.
    adjlist = list(map(lambda x: x.div(dyad_obs), adjlist))
    return adjlist

def dsi_table(adj_list, indiv, affiliative_behaviors, behav_obs, tot_obs):
    """Computes the DSI from the dataframe list and empty the diagonals."""
    dsi = pd.DataFrame(0, index=indiv, columns=indiv)
    for i in range(len(affiliative_behaviors)):
        dsi += (adj_list[i] / (behav_obs / tot_obs)
                [affiliative_behaviors[i]]) / len(affiliative_behaviors)
    # The diagonal is emptied.
    np.fill_diagonal(dsi.values, 0)
    return dsi

def affiliative_networks_adj(etho_obj):
    """Construct the affiliative networks adjacency matrices.

    This function first processes oriented and non-oriented behavior separately for format reasons.
    Then the adjacency matrices are computed using the private functions _length_adj, 
    _adj_table, _undir_adj_table, _table_list and _dsi_table.

    Returns
    -------
    adjlist : list of dataframe
        List of behavioral affiliative network adjacency matrices.
    undir_adjlist : list of dataframe
        List of behavioral affiliative network adjacency matrices in an undirected version.
    dsi : dataframe
        The DSI network adjacency matrix.
    dir_dsi : dataframe
        The DSI network adjacency matrix in an undirected version.
    """

    # The data, individual list and affiliative behaviors list are charged in local variables.
    data = etho_obj.data
    indiv = etho_obj.indiv
    affiliative_behaviors = etho_obj.affiliative_behaviors

    # Useful duration values are retrieved.
    dyad_obs, tot_obs, behav_obs = etho_obj._length_adj(
        data, indiv, affiliative_behaviors)

    # Undirected case.
    undir_adj = pd.DataFrame(data.loc[data['Behavior'].isin(['Etreinte', 'Jeu social', 'Contact passif'])].groupby(['Behavior', 'Subject', 'Modifiers'])[
                             'Duration (s)'].sum())  # The duration is calculated for each combination of behavior, individual, and modifiers.
    undir_adj = undir_adj.merge(pd.Series(undir_adj.index.get_level_values('Modifiers'), index=undir_adj.index).str.split(
        ',', expand=True), left_index=True, right_index=True)  # The names in the modifiers section are separated.
    undir_adj = undir_adj.replace('NaN', np.nan)
    undir_adj2 = undir_adj.loc[:, ['Duration (s)', 0]].dropna().rename(
        columns={0: 'Modifiers'})  # undir_adj2 is used for the loop.
    # Modifiers correction.
    for i in range(1, len(undir_adj.columns) - 1):
        undir_adj2 = pd.concat((undir_adj2, undir_adj.loc[:, [
                               'Duration (s)', i]].dropna().rename(columns={i: 'Modifiers'})))
    undir_adj = undir_adj2.set_index(undir_adj2.index.droplevel(2)).groupby(
        ['Behavior', 'Subject', 'Modifiers']).sum()  # Summed values for Modifiers.
    # Directed case.
    dir_adj = pd.DataFrame(data.loc[data['Behavior'].isin(['Grooming'])].groupby(['Behavior', 'Subject', 'Modifiers'])[
                           'Duration (s)'].sum())  # The duration is calculated for each combination of behavior, individual, and modifiers.
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
    dir_adj = dir_adj.groupby(['Behavior', 'Subject', 'Modifiers']).sum()

    # The multi-index dataframes sumarizing the informations for all the affiliative behaviors are computed.
    adj = adj_table(undir_adj, dir_adj, affiliative_behaviors, indiv)
    undir_adj = undir_adj_table(adj)
    # The affiliative networks adjacency matrices are computed.
    adjlist = table_list(adj, affiliative_behaviors, dyad_obs)
    undir_adjlist = table_list(
        undir_adj, affiliative_behaviors, dyad_obs)
    dsi = dsi_table(undir_adjlist, indiv,
                          affiliative_behaviors, behav_obs, tot_obs)
    dir_dsi = dsi_table(
        adjlist, indiv, affiliative_behaviors, behav_obs, tot_obs)

    return adjlist, undir_adjlist, dsi, dir_dsi