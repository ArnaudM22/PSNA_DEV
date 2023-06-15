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
import Modules.focal_parsing as pars
import Modules.net_construction as constr
import random
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import Modules.legend_plot as leg_plt

list_data_sets = ['rhesus_2021', 'tonkean_2021', 'rhesus_2022']
"""
# saimiri oriented (a cause du None)
'test3105.xlsx'
# saimiri basique (virer la partie proximity association)
'testmanquedirection3005.xlsx'
"""

data = pd.read_excel('../Data/datastream/tonkean_2021.xls')
data = data.drop(columns=['Unnamed: 0'])
indiv = pars.indiv_list(data)

affiliative_interactions, proximity_association,  agonistic_interactions, directed_interaction = pars.behaviors_list_def(
    data)

'Behavioral category'
behav_li = sorted(list(dict.fromkeys(data.loc[:, 'Behavior'])))
col_list = list(mcolors.TABLEAU_COLORS.values())
col_list.append('k')
col_list.append('peachpuff')
col_list.append('b')
col_list.append('g')
col_list.append('r')
col_list.append('m')
col_list.append('cornflowerblue')


def datastream_viz(data, n_line, n_column, behav_col='Behavior', col_list=None):
    # liste de comportements d'interet
    behav_li = sorted(list(dict.fromkeys(data.loc[:, behav_col])))
    if col_list == None:
        # random choice of colors
        col_list = list(mcolors.CSS4_COLORS.values())
        random.shuffle(col_list)
        col_list[:len(behav_li)]
    col_dict = {behav_li[i]: col_list[i] for i in range(len(behav_li))}
    # plot legend
    leg_plt.plot_colortable(col_dict, ncols=3, sort_colors=False)
    plt.show()
    # The data and individual list are charged in local variables to facilitate debugging.
    indiv = sorted(tuple(dict.fromkeys(data.loc[:, 'Subject'])))

    # A "plot_data" table is initialized.
    iterables = [list(dict.fromkeys(data.loc[:, 'numfocal'])), list(
        dict.fromkeys(data.loc[:, behav_col]))]  # Index content.
    # Index initialization.
    index = pd.MultiIndex.from_product(
        iterables, names=['numfocal', behav_col])
    plot_data = pd.DataFrame(index=index)  # initialiser dataframe
    # The data to plot are calculated.
    # Number of occurence.
    nbr_occur = data.groupby(
        ['numfocal', behav_col]).size().rename('nbr_occur')
    # Table filling.
    plot_data = plot_data.merge(
        nbr_occur, right_index=True, left_index=True, how='left')
    plot_data = plot_data.merge(data.groupby('numfocal')['Subject'].first(
    ), on='numfocal', how='left').set_axis(plot_data.index)  # Individual ID is added.
    plot_data = plot_data.fillna(0)  # Nan are replaced by 0.
    # Individual ID is set as an index level.
    plot_data = plot_data.set_index('Subject', append=True)
    # The data for the stacked bar plot are calculated.
    plot_indiv_data = plot_data.groupby(
        ['Subject', behav_col]).sum()  # on somme
    # For pei charts
    plt.rcParams.update({'font.size': 8,
                         'axes.titlepad': 0})
    plot_indiv_data = plot_indiv_data.unstack(level=0)
    plot_indiv_data.plot(kind='pie', subplots=True, layout=(
        n_line, n_column), legend=False, sharex=False, labels=None, title=indiv, ylabel='', colors=col_list)  # plot pour indiv
    plt.rcParams.update(plt.rcParamsDefault)
    # For stacked bar plots.
    fig, axs = plt.subplots(n_line, n_column)
    l = 0
    for a in range(n_line):
        for b in range(n_column):
            if l < (len(indiv)):
                plot_data2 = plot_data.loc[plot_data.index.get_level_values(
                    'Subject') == indiv[l]].unstack(level=1)
                plot_data2.plot(
                    ax=axs[a, b], kind='bar', stacked=True, legend=False, xlabel='', fontsize=2, color=col_list)  # Plot construction.
                # xticks Parameters.
                axs[a, b].tick_params(
                    axis='both', labelbottom=False, bottom=False, which='major', pad=0)
                # Title parameters.
                axs[a, b].set_title(indiv[l], pad=0, fontsize=10)
                l += 1
            else:
                axs[a, b].axis('off')
    plt.show()


datastream_viz(data, n_line=6, n_column=4, behav_col='Behavioral category 2')


def time_budg_construction(data, n_line, n_column, col_list, type_time_budg='whole'):
    """"Builds the set of pie charts and stacked bar plot"""

    if type_time_budg == 'number of events':
        data.loc[:, 'Duration (s)'] = 1

    if type_time_budg == 'length of state':
        data = data.loc[data['Behavior type'] == 'SCAN']

    # The data and individual list are charged in local variables to facilitate debugging.
    indiv = sorted(tuple(dict.fromkeys(data.loc[:, 'Subject'])))

    # A "plot_data" table is initialized.
    iterables = [list(dict.fromkeys(data.loc[:, 'numfocal'])), list(
        dict.fromkeys(data.loc[:, 'Behavior']))]  # Index content.
    # Index initialization.
    index = pd.MultiIndex.from_product(
        iterables, names=['numfocal', 'Behavior'])
    plot_data = pd.DataFrame(index=index)  # initialiser dataframe
    # The data to plot are calculated.
    # Number of occurence.
    nbr_occur = data.groupby(
        ['numfocal', 'Behavior']).size().rename('nbr_occur')
    # Table filling.
    plot_data = plot_data.merge(
        nbr_occur, right_index=True, left_index=True, how='left')
    plot_data = plot_data.merge(data.groupby('numfocal')['Subject'].first(
    ), on='numfocal', how='left').set_axis(plot_data.index)  # Individual ID is added.
    plot_data = plot_data.fillna(0)  # Nan are replaced by 0.
    # Individual ID is set as an index level.
    plot_data = plot_data.set_index('Subject', append=True)
    # The data for the stacked bar plot are calculated.
    plot_indiv_data = plot_data.groupby(
        ['Subject', 'Behavior']).sum()  # on somme
    # For pei charts
    plt.rcParams.update({'font.size': 8,
                         'axes.titlepad': 0})
    plot_indiv_data = plot_indiv_data.unstack(level=0)
    plot_indiv_data.plot(kind='pie', subplots=True, layout=(
        n_line, n_column), legend=False, sharex=False, labels=None, title=indiv, ylabel='', colors=col_list)  # plot pour indiv
    plt.rcParams.update(plt.rcParamsDefault)
    # For stacked bar plots.
    fig, axs = plt.subplots(n_line, n_column)
    l = 0
    for a in range(n_line):
        for b in range(n_column):
            if l < (len(indiv)):
                plot_data2 = plot_data.loc[plot_data.index.get_level_values(
                    'Subject') == indiv[l]].unstack(level=1)
                plot_data2.plot(
                    ax=axs[a, b], kind='bar', stacked=True, legend=False, xlabel='', fontsize=2, color=col_list)  # Plot construction.
                # xticks Parameters.
                axs[a, b].tick_params(
                    axis='both', labelbottom=False, bottom=False, which='major', pad=0)
                # Title parameters.
                axs[a, b].set_title(indiv[l], pad=0, fontsize=10)
                l += 1
            else:
                axs[a, b].axis('off')
    plt.show()


time_budg_construction(data, n_line=6, n_column=4,
                       col_list=col_list, type_time_budg='number of events')


social_behaviors = affiliative_interactions + \
    agonistic_interactions + proximity_association


# first : visualisation
"""data viz"""
# a reprendre
"""viz.visualisation(data, 5, 5)"""


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
                                                 directed_interaction, affiliative_interactions, indiv, undir_adj_table=True)
# dsi
behavior_rate_list = list(affiliative_behavior_rate_dict.values())
behav_obs = pars.behav_obs_time(data, affiliative_interactions)
tot_obs = pars.tot_obs_time(data)
dsi = constr.dsi_table(
    behavior_rate_list, indiv, affiliative_interactions, behav_obs, tot_obs)
"""
a = stat.indiv_properties(dsi)
net = nx.Graph(dsi)
nx.draw(net)
nx.eigenvector_centrality(net)
nx.is_weighted(net)"""

behavior_rate_dict['dsi'] = dsi
with pd.ExcelWriter('../Data/layers_rhesus_2022_NO.xlsx') as writer:
    for df_name, df in behavior_rate_dict.items():
        df.to_excel(writer, sheet_name=df_name)
