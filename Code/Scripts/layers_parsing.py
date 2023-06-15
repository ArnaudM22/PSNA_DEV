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
import seaborn

list_data_sets = ['rhesus_2021', 'tonkean_2021', 'rhesus_2022', 'sai_2023']
dataset_name = 'rhesus_2022'


"""
# saimiri oriented (a cause du None)
'test3105.xlsx'
# saimiri basique (virer la partie proximity association)
'testmanquedirection3005.xlsx'
"""
"""
observer stats for saimiri
data = pd.read_excel('../Data/datastream/' + dataset_name + '.xls')
data = data.drop(columns=['Unnamed: 0'])
indiv = pars.indiv_list(data)
obs = data.groupby('numfocal')['Observer'].first()
assistant = data.groupby('numfocal')['Assistant'].first()
"""

affiliative_interactions, proximity_association,  agonistic_interactions, directed_interaction = pars.behaviors_list_def(
    data)

directed_interaction = []
social_behaviors = affiliative_interactions + \
    agonistic_interactions + proximity_association


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


if dataset_name == 'sai_2023':
    behav_col = 'Behavior'
else:
    behav_col = 'Behavioral category 2'
# visualisation
datastream_viz(data, n_line=6, n_column=4, behav_col=behav_col)


"""parsing"""
ind_obs = pars.ind_obs_time(data)
ind_obs.plot(kind='bar')
plt.show()
dyad_obs = pars.dyad_obs_time(data, indiv)
# autre façon de représenter : reorga avec lignes et colonnes qui ont la somme la plus petite
mat = dyad_obs.copy(deep=True)
mat.loc["mean"] = mat.mean(0)
mat.loc[:, "mean"] = mat.mean(0)
mat.sort_values("mean", ascending=False, inplace=True)
mat.sort_values("mean", ascending=False, axis=1, inplace=True)
mat.drop("mean", inplace=True)
mat.drop("mean", axis=1, inplace=True)
seaborn.heatmap(mat)
plt.show()
tot_time = pars.tot_obs_time(data)
pars.behav_obs_time(data, affiliative_interactions)
# edge_list pour les non-orientés : toujours non-symetrique. Pose question de si bien reciproque ?
pars.edge_list(data, social_behaviors)
pars.adj_table(data, directed_interaction,
               social_behaviors, indiv, undir_adj_table=True)
# mettre en dict, dissocier les calculs de taux, l'empty diagonal.
behavior_rate_dict = pars.table_dict(data, affiliative_interactions,
                                     directed_interaction, social_behaviors, indiv, undir_adj_table=True)
affiliative_behavior_rate_dict = pars.table_dict(data, affiliative_interactions,
                                                 directed_interaction, affiliative_interactions, indiv, undir_adj_table=True)
# dsi
behavior_rate_list = list(affiliative_behavior_rate_dict.values())
behav_obs_time = pars.behav_obs_time(data, affiliative_interactions)
behav_obs_count = pars.behav_obs_count(data, affiliative_interactions)
tot_obs = pars.tot_obs_time(data)
dsi = constr.dsi_table2(
    behavior_rate_list, indiv, affiliative_interactions, behav_obs_time, tot_obs)
behavior_rate_dict['dsi'] = dsi
"""save
with pd.ExcelWriter('../Data/layers_' + dataset_name + '.xlsx') as writer:
    for df_name, df in behavior_rate_dict.items():
        df.to_excel(writer, sheet_name=df_name)
"""