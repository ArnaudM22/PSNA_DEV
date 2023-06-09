# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 12:19:25 2023

@author: arnaud.maupas
"""
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

def visualisation(etho_obj, n_line, n_column, see_table=False):
    """Performs basic exploratory visualizations.

    This function allows to build :
    1. A table of behaviors with all the behaviors, their number of occurrences, 
    their behavioral categories (type I and II, with each time the corresponding number of occurrences).
    2. A set of piecharts showing the proportion of the number of occurrence of 
    each behavioral category (type II) for each individual.
    3. A set of stacked bar plots for each individual showing the proportion of 
    the number of occurrences of each behavioral category (type II), where each bar represents a focal.   

    Parameters
    ----------
    n_line : int
        Number of lines on the plot.
    n_column : int
        Number of columns on the plot.
    see_table : bool, optional
        Specifies whether to display the behavioral table. The default is False.

    Returns
    -------
    None.
    """

    def behavior_table_construction(see_table):
        """Builds the behavioral table"""

        # The data are charged in a local variable.
        data = etho_obj.data.copy(deep=True)

        # The qualitative version of the behaviorial table is built.
        behavior_table = data.groupby(
            'Behavior')[['Behavioral category', 'Behavioral category 2']].first()
        # The number of occurence of the behaviors and behavioral categories is added.
        behavior_table.insert(0, 'n', behavior_table.index)
        behavior_table.loc[:, 'n'] = behavior_table.apply(
            lambda row:  str(Counter(data.loc[:, 'Behavior'])[row.n]), axis=1)
        behavior_table.loc[:, 'Behavioral category'] = behavior_table.apply(
            lambda row: row['Behavioral category'] + ': n=' + str(Counter(data.loc[:, 'Behavioral category'])[row['Behavioral category']]), axis=1)
        behavior_table.loc[:, 'Behavioral category 2'] = behavior_table.apply(
            lambda row: row['Behavioral category 2'] + ': n=' + str(Counter(data.loc[:, 'Behavioral category 2'])[row['Behavioral category 2']]), axis=1)
        # Table displaying (optional).
        if see_table == True:
            print(behavior_table)

    def time_budg_construction(n_line, n_column):
        """"Builds the set of pie charts and stacked bar plot"""

        # The data and individual list are charged in local variables to facilitate debugging.
        indiv = etho_obj.indiv
        data = etho_obj.data

        # A "plot_data" table is initialized.
        iterables = [list(dict.fromkeys(data.loc[:, 'numfocal'])), list(
            dict.fromkeys(data.loc[:, 'Behavioral category 2']))]  # Index content.
        # Index initialization.
        index = pd.MultiIndex.from_product(
            iterables, names=['numfocal', 'Behavioral category 2'])
        plot_data = pd.DataFrame(index=index)  # initialiser dataframe
        # The data to plot are calculated.
        # Number of occurence.
        nbr_occur = data.groupby(
            ['numfocal', 'Behavioral category 2']).size().rename('nbr_occur')
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
            ['Subject', 'Behavioral category 2']).sum()  # on somme
        # For pei charts
        plt.rcParams.update({'font.size': 8,
                             'axes.titlepad': 0})
        plot_indiv_data.unstack(level=0).plot(kind='pie', subplots=True, layout=(
            n_line, n_column), legend=False, sharex=False, labels=None, title=indiv, ylabel='')  # plot pour indiv
        plt.rcParams.update(plt.rcParamsDefault)
        # For stacked bar plots.
        fig, axs = plt.subplots(n_line, n_column)
        l = 0
        for a in range(n_line):
            for b in range(n_column):
                if l < (len(indiv)):
                    plot_data.loc[plot_data.index.get_level_values('Subject') == indiv[l]].unstack(level=1).plot(
                        ax=axs[a, b], kind='bar', stacked=True, legend=False, xlabel='', fontsize=2)  # Plot construction.
                    # xticks Parameters.
                    axs[a, b].tick_params(
                        axis='both', labelbottom=False, bottom=False, which='major', pad=0)
                    # Title parameters.
                    axs[a, b].set_title(indiv[l], pad=0, fontsize=10)
                    l += 1
                else:
                    axs[a, b].axis('off')
        plt.show()

    behavior_table_construction(see_table)
    time_budg_construction(n_line, n_column)
