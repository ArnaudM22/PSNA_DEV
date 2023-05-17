# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 16:24:17 2023

@author: arnaud.maupas
"""

import pandas as pd
import itertools
import seaborn
import Modules.net_stat as net
import numpy as np
import matplotlib.pyplot as plt
import Modules.class_definition as class_def
import Modules.focal_cleaning as clean
import Modules.net_viz as viz
import Modules.focal_parsing as pars
import Modules.net_construction as constr


"""(for example, the eigenvector-centrality-based RDM for a given participant), 
the variance accounted for by the remaining two predictor RDMs (for example 
the social distance and constraint-based RDMs for that participant) was 
removed using ordinary least squares regression. Thus, the resultant predictor 
RDMs were made orthogonal to one another prior to performing the GLM 
decomposition searchlight.
Because RDMs are symmetric about a diagonal of zeros, all RDMs were 
flattened to form vectors of their above-diagonal elements prior to performing 
the steps described above (that is, prior to z-scoring, orthogonalization and GLM 
decomposition)."""


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

rhesus2022 = class_def.Focals('../Data/Raw/Rhesus_2022_xls',
                              open_preprocessed=False, check_empty_col=True, ignore=())

# Manual adjustment : renommer Groom.er.ee -> Ind
rhesus2022.data = rhesus2022.data.drop(np.where(
    rhesus2022.data['Behavior'] == '4 Position')[0]).reset_index(drop=True)

rhesus2022.filtering(grooming_see=True, non_visible_see=True,
                     short_focal_preprocessing_see=True, save=None, ignore=())  # filtering

rhesus2022.data = clean.social_category(rhesus2022.data, affiliative_interactions=affiliative_interactions, agonistic_interactions=[
], proximity_association=proximity_association)
rhesus2022.data = clean.interactor_direction(rhesus2022.data, directed_interaction=directed_interaction,
                                             undirected_interaction=undirected_interaction, proximity_association=proximity_association)
rhesus2022.data = clean.column_reorder(rhesus2022.data)
"""parsing"""
pars.ind_obs_time(rhesus2022.data)
a = pars.dyad_obs_time(rhesus2022.data, rhesus2022.indiv)
pars.ind_obs_time(rhesus2022.data)
pars.tot_obs_time(rhesus2022.data)
pars.behav_obs_time(rhesus2022.data, affiliative_interactions)
# edge_list pour les non-orientés : toujours non-symetrique. Pose question de si bien reciproque ?
pars.edge_list(rhesus2022.data, social_behaviors)
pars.adj_table(rhesus2022.data, directed_interaction,
               social_behaviors, rhesus2022.indiv, undir_adj_table=True)
# mettre en dict, dissocier les calculs de taux, l'empty diagonal.
behavior_rate_dict = pars.table_dict(rhesus2022.data, affiliative_interactions,
                                     directed_interaction, social_behaviors, rhesus2022.indiv, undir_adj_table=True)

"""look at proximity"""
# première étape: repets
prox = rhesus2022.data
prox = prox.loc[prox['Social behavior category'] == 'Proximity association']
scan_count = prox.loc[prox['Behavior'] == '0. Debut du scan']
scan_count = scan_count.groupby('numfocal').sum('Duration (s)')

"""network construction"""
behavior_rate_list = list(behavior_rate_dict.values())
behav_obs = pars.behav_obs_time(tonkean_focals.data, affiliative_interactions)
tot_obs = pars.tot_obs_time(tonkean_focals.data)


dsi = constr.dsi_table(
    behavior_rate_list, rhesus2022.indiv, affiliative_interactions, behav_obs, tot_obs)

'''
dsi[dsi != 0] = 1
dsi.to_numpy().sum()

viz.visualisation(rhesus2022, see_table=True, n_line=5, n_column=4)
'''


def RDM(dataframe, indiv, plot=True):

    def pairwise_eucl(values):
        # Dataframe pairwise
        mat = [abs(x-y) for x, y in itertools.product(values, repeat=2)]
        mat = np.array(mat).reshape(len(values), len(values))
        # z-scoring
        mat = (mat-np.mean(mat, axis=(0, 1), keepdims=True)) / \
            np.std(mat, axis=(0, 1), keepdims=True)
        mat = pd.DataFrame(mat, index=values.index, columns=values.index)
        # reorganisation
        mat.sort_index(axis=0, inplace=True)
        mat.sort_index(axis=1, inplace=True)
        ''' #cas par somme globale
        mat.loc["mean"] = mat.mean(0)
        mat.loc[:, "mean"] = mat.mean(0)
        mat.sort_values("mean", inplace=True)
        mat.sort_values("mean", axis=1, inplace=True)
        mat.drop("mean", inplace=True)
        mat.drop("mean", axis=1, inplace=True)
        '''

        return mat

    # recuperer propriétés individuelles
    RDM_dict = net.indiv_properties(dataframe)
    # supprimer djikstra
    del RDM_dict["Distance_weight"]
    # recuperer distance par rapport à individu
    RDM_dict["Distance"] = RDM_dict["Distance"].loc[:, indiv]
    # enlever individu du jeu de donnée
    RDM_dict = {k: v.drop(indiv) for k, v in RDM_dict.items()}
    # remplacer par z-scored pairwise matrix
    RDM_dict = {k: pairwise_eucl(v) for k, v in RDM_dict.items()}

    if plot == True:
        met_list = ["Centrality", "Brokerage", "Distance"]
        col_list = ["Reds", "Greens", "Purples"]

        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        for i in range(3):
            axs[i].set_title(met_list[i])
            axs[i].tick_params(axis='both', which='major', labelsize=10)
            seaborn.heatmap(RDM_dict[met_list[i]], cmap=col_list[i], ax=axs[i], cbar_kws={'location': 'bottom',
                                                                                          'ticks': [RDM_dict[met_list[i]].to_numpy().min() + 0.25, RDM_dict[met_list[i]].to_numpy().max() - 0.25]})
            axs[i].collections[0].colorbar.set_ticklabels(
                ["Similar", "Dissimilar"])
            axs[i].collections[0].colorbar.ax.tick_params(size=0)

        fig.suptitle("Observed individual : " + indiv)
        plt.show()

    return RDM_dict


dict_prop = net.indiv_properties(dsi)
seaborn.clustermap(dict_prop['Distance'], method='complete',
                   metric='euclidean', dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
seaborn.clustermap(dict_prop['Distance_weight'], method='complete',
                   metric='euclidean', dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

for indiv in ['Theoden', 'Spliff', 'Vladimir', 'Yvan', 'Boromir', 'Faramir', 'Djocko']:
    RDM(dsi, indiv)
