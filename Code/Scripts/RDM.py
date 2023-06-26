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
        mat.loc["mean"] = mat.mean(0)
        mat.loc[:, "mean"] = mat.mean(0)
        mat.sort_values("mean", inplace=True)
        mat.sort_values("mean", axis=1, inplace=True)
        mat.drop("mean", inplace=True)
        mat.drop("mean", axis=1, inplace=True)

        return mat

    # recuperer propriétés individuelles
    RDM_dict = net.indiv_properties(dataframe)
    # recuperer distance par rapport à individu
    RDM_dict["Distance"] = RDM_dict["Distance"].loc[:, indiv]
    RDM_dict["Distance_weight"] = RDM_dict["Distance_weight"].loc[:, indiv]
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


# ouverture jeu de données:
data = pd.read_excel('../Data/layers/layers_rhesus_2022.xlsx', 'Grooming', index_col = 'Other individual')

for indiv in ['Theoden', 'Spliff', 'Vladimir', 'Yvan']:
    RDM(data,indiv , plot=True)

